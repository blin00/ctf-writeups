import re
from binascii import hexlify
from z3 import *

def nightmare_r(blob, arg2, arg3):
    assert len(blob) == 0x64
    rax_4 = blob[0x63] ^ arg2
    table = set([
        0x0c, 0x09, 0x06, 0x05, 0x04, 0x03, 0x01, 0x00,
        0x1c, 0x19, 0x16, 0x15, 0x14, 0x13, 0x10, 0x0d,
        0x34, 0x32, 0x2e, 0x2d, 0x2a, 0x29, 0x26, 0x25,
        0x41, 0x40, 0x3f, 0x3d, 0x3c, 0x3a, 0x38, 0x36,
        0x52, 0x51, 0x50, 0x4f, 0x48, 0x47, 0x43, 0x42,
        0x5f, 0x5e, 0x5c, 0x5b, 0x5a, 0x59, 0x58, 0x57,
        0x61, 0x60,
    ])

    res = [None] * 0x64
    for i in range(0x64):
        if i == 0:
            res[i] = 0
        else:
            res[i] = blob[i - 1]
        if i in table:
            res[i] ^= rax_4
        # if arg3 != 0:
        #     res[i] ^= blob[i]
        if isinstance(arg3, int):
            res[i] = res[i] ^ (blob[i] & arg3)
        else:
            # res[i] = res[i] ^ (blob[i] & arg3)
            # faster somehow??
            res[i] = If(arg3 != 0, res[i] ^ blob[i], res[i])
    return res

def nightmare_r_z3(blob, arg2, arg3):
    assert len(blob) == 0x64
    rax_4 = Xor(blob[0x63], arg2)
    table = set([
        0x0c, 0x09, 0x06, 0x05, 0x04, 0x03, 0x01, 0x00,
        0x1c, 0x19, 0x16, 0x15, 0x14, 0x13, 0x10, 0x0d,
        0x34, 0x32, 0x2e, 0x2d, 0x2a, 0x29, 0x26, 0x25,
        0x41, 0x40, 0x3f, 0x3d, 0x3c, 0x3a, 0x38, 0x36,
        0x52, 0x51, 0x50, 0x4f, 0x48, 0x47, 0x43, 0x42,
        0x5f, 0x5e, 0x5c, 0x5b, 0x5a, 0x59, 0x58, 0x57,
        0x61, 0x60,
    ])

    res = [None] * 0x64
    for i in range(0x64):
        if i == 0:
            res[i] = False
        else:
            res[i] = blob[i - 1]
        if i in table:
            res[i] = Xor(res[i], rax_4)
        res[i] = If(arg3, Xor(res[i], blob[i]), res[i])
    return res

var_2b8_raw = [
    0x10100000000,
    0x1010101000100,
    0x100010001000001,
    0x1010001000100,
    0x1000001,
    0x100010001000000,
    0x1000000000100,
    0x1010101000001,
    0x101010001000100,
    0x100010101010101,
    0x1010101010100,
    0x10001,
    0x10100,
]

var_248_raw = [
    0x100000101000100,
    0x100000101010100,
    0x1010000000100,
    0x101000101010001,
    0x1010000000101,
    0x101010001,
    0x100010000000100,
    0x101010000000101,
    0x101000100010101,
    0x10101010001,
    0x101000000000100,
    0x100000100000001,
    1,
]

var_1d8_raw = [
    0x100010001010101,
    0x1010101010101,
    0x101010101000100,
    0x100000101010101,
    0x100000000000001,
    0x100000100000101,
    0x1000001000100,
    0x100010001010101,
    0x100,
    0x1000101000000,
    0x101010001010000,
    0x100000101010000,
    1,
]

var_168_raw = [
    0x1010100010101,
    0x100010101000000,
    0x100000001010000,
    0x1000001010000,
    0x1010000000101,
    0x100010100000000,
    0x100000001,
    0x1000001000001,
    0x10001000101,
    0x101000000010001,
    0x101010101000101,
    0x1000000000000,
    0x1000000,
]

def unpack(raw):
    res = []
    assert len(raw) == 13
    for i in range(12):
        x = raw[i]
        for j in range(8):
            y = x & 0xff
            x >>= 8
            res.append(y)
    x = raw[12]
    for j in range(4):
        y = x & 0xff
        x >>= 8
        res.append(y)
    assert len(res) == 0x64
    return res

var_2b8 = unpack(var_2b8_raw)
var_248 = unpack(var_248_raw)
var_1d8 = unpack(var_1d8_raw)
var_168 = unpack(var_168_raw)

def nightmare_s(blob, arg2, arg3):
    rax_4 = blob[0x63] ^ arg2

    partial = [None] * 0x64
    partial[0] = 0
    partial[0x63] = blob[0x62]
    for i in range(1, 0x63):
        partial[i] = blob[i - 1] ^ ((var_248[i] ^ blob[i + 1]) & (blob[i] ^ var_2b8[i]))

    res = [None] * 0x64
    for i in range(0x64):
        if isinstance(arg3, int):
            res[i] = var_168[i] ^ partial[i] ^ rax_4 if arg3 != 0 else var_1d8[i] ^ partial[i] ^ rax_4
        else:
            if var_168[i] == var_1d8[i]:
                res[i] = var_168[i] ^ partial[i] ^ rax_4
            # elif var_168[i] == 1:
            #     res[i] = arg3 ^ partial[i] ^ rax_4
            # else:
            #     res[i] = arg3 ^ partial[i] ^ rax_4 ^ 1
            else:
                res[i] = If(arg3 != 0, var_168[i] ^ partial[i] ^ rax_4, var_1d8[i] ^ partial[i] ^ rax_4)
    return res

def nightmare_s_z3(blob, arg2, arg3):
    rax_4 = Xor(blob[0x63], arg2)

    partial = [None] * 0x64
    partial[0] = False
    partial[0x63] = blob[0x62]
    for i in range(1, 0x63):
        partial[i] = Xor(
            blob[i - 1],
            And(Xor(bool(var_248[i]), blob[i + 1]), Xor(blob[i], bool(var_2b8[i])))
        )

    res = [None] * 0x64
    for i in range(0x64):
        t = Xor(partial[i], rax_4)
        res[i] = Xor(If(arg3, bool(var_168[i]), bool(var_1d8[i])), t)
    return res

def nightmare(arg1, arg2, arg3, arg4):
    rax_6 = arg1[0xe] ^ arg2[1]
    rax_12 = arg1[4] ^ arg2[0x33]
    if arg3 == 0:
        var_c = arg4
    else:
        var_c = arg2[0x32] ^ arg4
    return nightmare_r(arg1, var_c, rax_6), nightmare_s(arg2, arg4, rax_12)

def nightmare_z3(arg1, arg2, arg3, arg4):
    rax_6 = Xor(arg1[0xe], arg2[1])
    rax_12 = Xor(arg1[4], arg2[0x33])
    arg4 = bool(arg4)
    if arg3 == 0:
        var_c = arg4
    else:
        var_c = Xor(arg2[0x32], arg4)
    return nightmare_r_z3(arg1, var_c, rax_6), nightmare_s_z3(arg2, arg4, rax_12)

def create_dream(blob1, blob2, n):
    blob1 = list(map(int, blob1))
    blob2 = list(map(int, blob2))
    res = []
    for i in range(n):
        x = 0
        for j in range(8):
            bit = blob1[0] ^ blob2[0]
            x |= bit << j
            blob1, blob2 = nightmare(blob1, blob2, 0, 0)
        res.append(x)
    return bytes(res), blob1, blob2

def create_dream_z3(blob1, blob2, n):
    res = []
    for i in range(n):
        for j in range(8):
            bit = Xor(blob1[0], blob2[0])
            res.append(bit)
            blob1, blob2 = nightmare_z3(blob1, blob2, 0, 0)
    return res, blob1, blob2

def bytes_to_bits(L):
    res = []
    for i in range(13):
        for j in range(8 if i < 12 else 4):
            res.append((L[i] >> j) & 1)
    return res

def try_reverse(s1, s2, ct, pt):
    blob1_orig = [Bool(f'blob1_{i}') for i in range(0x64)]
    blob2_orig = [Bool(f'blob2_{i}') for i in range(0x64)]
    bits, blob1, blob2 = create_dream_z3(blob1_orig, blob2_orig, 1)
    s = Solver()
    assert len(bits) == 8
    assert isinstance(ct, int)
    if pt is None:
        s.add(bits[7] == bool((ct >> 7) & 1))
    else:
        assert isinstance(pt, int)
        for i in range(8):
            s.add(bits[i] == bool(((pt ^ ct) >> i) & 1))
    for i in range(0x64):
        s.add(blob1[i] == bool(s1[i]))
        s.add(blob2[i] == bool(s2[i]))
    res = []
    while s.check() == sat:
        m = s.model()
        dedup = []
        A = []
        B = []
        for x in blob1_orig:
            dedup.append(x == m[x])
            A.append(bool(m[x]))
        for x in blob2_orig:
            dedup.append(x == m[x])
            B.append(bool(m[x]))
        res.append((tuple(A), tuple(B)))
        s.add(Not(And(*dedup)))
    return res

if __name__ == '__main__':
    with open('flag.txt.enc', 'rb') as f:
        enc = f.read()
    s1, s2 = enc[-26:-13], enc[-13:]
    s1 = bytes_to_bits(s1)
    s2 = bytes_to_bits(s2)
    t_len = len(enc) - 26
    print('ciphertext len:', t_len)
    possible = set([(tuple(s1), tuple(s2))])
    for i in range(t_len):
        print('num possible:', len(possible))
        new_possible = set()
        for s1, s2 in possible:
            res = try_reverse(s1, s2, enc[t_len - 1 - i], None)
            new_possible.update(res)
        possible = new_possible
        brain = set()
        for s1, s2 in possible:
            r = b''
            ks, _, _ = create_dream(s1, s2, i + 1)
            for a, b in zip(ks, enc[t_len - 1 - i:t_len]):
                r += bytes([a ^ b])
            brain.add(r)
        print(brain)
