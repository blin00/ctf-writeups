#!/usr/bin/env python3

from pwn import *
import json
import sys
from lib import dff

if len(sys.argv) > 1 and sys.argv[1].lower().startswith('r'):
    io = remote('hwsim.2024.ctfcompetition.com', 1337)
else:
    io = process(['python3', 'hwsim.py'])

def parse(fname):
    with open(fname, 'r') as f:
        adder = json.load(f)
    circuit = adder['modules']['circuit']
    ports = circuit['ports']
    cells = circuit['cells']
    A = ports['a']['bits'][0]
    B = ports['b']['bits'][0]
    C = ports['c_in']['bits'][0]
    S = ports['s']['bits'][0]
    Cout = ports['c_out']['bits'][0]
    clk = ports['clk']['bits'][0]
    gates = [
        ('B^', 'B', 'B'),
        ('clk', 'clk^', 'clk^'),
        ('clk^', 'clk2', 'clk2'),
        ('clk2', 'clk2^', 'clk2^'),
        ('clk2^', 'clk3', 'clk3'),
        ('clk3', 'clk3^', 'clk3^'),
        ('clk3^', 'A', 'B^'),
        ('clk_buf^', 'clk', 'clk'),
        ('clk_buf', 'clk_buf^', 'clk_buf^'),
        ('clk_clean^', 'clk', 'clk_buf'),
        ('clk_clean', 'clk_clean^', 'clk_clean^'),
    ]
    def map_id(x):
        if x == A:
            return 'A'
        if x == B:
            return 'B'
        if x == C:
            return 'C'
        if x == S:
            return 'S'
        if x == Cout:
            return 'Cout'
        if x == clk:
            return 'clk_clean'
        if not isinstance(x, int):
            raise ValueError(f'unknown id {x}')
        return str(x)
    dff_ct = 0
    for cell in cells.values():
        if cell['type'] == '$_NAND_':
            a = map_id(cell['connections']['A'][0])
            b = map_id(cell['connections']['B'][0])
            y = map_id(cell['connections']['Y'][0])
            gates.append((y, a, b))
        elif cell['type'] == '$_NOT_':
            a = map_id(cell['connections']['A'][0])
            y = map_id(cell['connections']['Y'][0])
            gates.append((y, a, a))
        elif cell['type'] == '$_DFF_P_':
            d = map_id(cell['connections']['D'][0])
            q = map_id(cell['connections']['Q'][0])
            c = map_id(cell['connections']['C'][0])
            gates += dff(f'dff_{dff_ct}', c, d, q)
            dff_ct += 1
        else:
            raise ValueError(f'unknown cell type {cell["type"]}')
    return gates

def solve(io):
    gates = parse('adder.json')
    print(f'sending {len(gates)} gates')
    for y, a, b in gates:
        io.recvuntil(b'5. Quit\n')
        io.sendline(b'3')
        io.sendline(f'{y} {a} {b}'.encode())
    print('running CPU')
    io.recvuntil(b'5. Quit\n')
    io.sendline(b'4')
    for i in range(50): # threshold here
        io.recvuntil(b'CPU is awaiting input character...\n')
        io.sendline(b'\x00')
    io.recvuntil(b'CPU is awaiting input character...\n')
    io.sendline()
    io.sendline(b'5')
    s = io.stream()
    lines = s.decode().strip().splitlines()
    res = ''
    for l in lines:
        if l.startswith('CPU outputs: '):
            res += l[13:]
    print(res)

# to get each half of the flag, change thresholds in this file and adder.v

# range(30), ctr > 30
# CTF{abcdefghijklmnopqrs??vw??z
# CTF{H4rdwar3_acc3ler4te??ba??d

# range(50), ctr > 70
# qrstuvwxyzABCDEFGHIJKLMNOPQRST
# ted_backd00rs_are_7he_w0rst}

# CTF{H4rdwar3_acc3ler4ted_backd00rs_are_7he_w0rst}

solve(io)
