#!/usr/bin/env python3

from binascii import unhexlify

raw = unhexlify('23384124435424435473243838414327412443547324383823514343435473232441243843435473233838514343244354732338384343542241732162940162b20162840139053f11f4ff2957810e406503003253323a395e57f3b4a38c7fba07406503003153313a62670162850162570139b77380e1b07287f203406503003253323a393f68a3e4049a3b8f07406503003153313a623a01625801622a01395427b5b695525dcd0b406503003253323a3928919a4aa271379107406503003153313a620d01622b0162fd0039a3861405418c74e50b406503003253323a39bc61edf2e96ec1ab06406503003153313a62e00062fe0062d0003988923ae0693f549206406503003253323a390fd1bee339a196c505406503003153313a62b30062d10062a3003983ea7b97e54cd3ea06406503003253323a3987efb0d15cfe86ad04406503003153313a62860062a4006276003919426cd4caf6f2d909406503003253323a39efffda1513eaaedb06406503003153313a62590062770062490039fe1397dfcd127ef00a406503003253323a391cafcf1f964541a506406503003153313a72233843254124384343546405003a3a637d003a395a883414a0c305bdfe3f648e00636b00323832383243324132617262420072623e00222241234343243841542438434354244354443852424331617262210072621d002222412343432438415424384343542443544438532241315243433161312338432343542241670f00243843244325412443546802003161232543244123384343547323244124384343547322234124384343547363210023224541243838434343547324382623412441434354732338432443547363000023384354737100')
raw = raw[:-1]    # strip the last null byte

def u16(b):
    assert len(b) == 2
    return int.from_bytes(b, 'little')

def disas(idx, op, arg):
    if op == 0:
        return 'fldz'
    elif op == 1:
        return 'fld1'
    elif op == 2:
        return 'fldpi'
    elif op == 3:
        return 'fldl2t'
    elif op == 4:
        return 'fldl2e'
    elif op == 5:
        return 'fldlg2'
    elif op == 6:
        return 'fldln2'
    elif 7 <= op <= 15:
        return 'ud2'
    elif op == 16:
        return 'fxch st0, st1'
    elif op == 17:
        return 'fxch st0, st2'
    elif op == 18:
        return 'fxch st0, st3'
    elif op == 19:
        return 'fxch st0, st4'
    elif op == 20:
        return 'fxch st0, st5'
    elif op == 21:
        return 'fxch st0, st6'
    elif op == 22:
        return 'fxch st0, st7'
    elif op == 23:  # duplicate top value of stack
        return 'fld st0'
        # return 'fst st7, st0; fdecstp'
    elif op == 24:
        return f'fld {hex(arg)}'
    elif op == 25:  # pop top value of stack
        return 'fstp st0'
        # return 'ffree st0; fincstp'
    elif 26 <= op <= 31:
        return 'ud2'
    elif op == 32:
        return 'faddp st1, st0'
    elif op == 33:
        return 'fsubp st1, st0'
    elif op == 34:
        return 'fmulp st1, st0'
    elif op == 35:
        return 'fdivp st1, st0'
    elif op == 36:
        return 'fchs'
    elif 37 <= op <= 47:
        return 'ud2'
    elif op == 48:
        return 'fsqrt'
    elif op == 49:
        return 'fsin'
    elif op == 50:
        return 'fcos'
    elif op == 51:
        return 'frndint'
    elif 52 <= op <= 63:
        return 'ud2'
    elif op == 64:  # fistp [mem]; jmp [mem]
        return 'ret'
    elif op == 65:
        return f'call {idx + 3 + arg}'
    elif op == 66:
        return f'jmp {idx + 3 + arg}'
    # fcomp st0, st1 (pops one element off stack)
    elif op == 67:
        return f'je {idx + 3 + arg}'
    elif op == 68:
        return f'jne {idx + 3 + arg}'
    elif op == 69:
        return f'jae {idx + 3 + arg}'
    elif op == 70:
        return f'ja {idx + 3 + arg}'
    elif op == 71:
        return f'jbe {idx + 3 + arg}'
    elif op == 72:
        return f'jb {idx + 3 + arg}'
    elif 73 <= op <= 79:
        return 'ud2'
    elif op == 80:
        return 'exit'
    elif op == 81:
        return 'read'   # pushes integer value onto stack, or negative 1 if eof
    elif op == 82:
        return 'write'  # pops integer value off of stack
    else:
        assert False

code = []

idx = 0
while idx < len(raw):
    inst_idx = idx
    op = raw[idx]
    idx += 1
    arg = None
    op -= 0x21
    op &= 0xff
    if op == 0x18:
        arg = int.from_bytes(raw[idx:idx + 10], 'little')
        idx += 10
    elif (op - 0x41) & 0xff <= 0xd:
        arg = u16(raw[idx:idx + 2])
        idx += 2

    assert 0 <= op <= 0x52, op
    code.append((inst_idx, op, arg))

for tup in code:
    print(f'{tup[0]}:', disas(*tup))
