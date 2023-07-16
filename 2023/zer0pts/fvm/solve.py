#!/usr/bin/env python3

# must be run on a platform that supports 80 bit long double
# aka not windows

import numpy as np

cons = [
    # a * b, a + b
    (0x400e815729fff4113f05, 0x4007ba7f8ca3b4f3575e),
    (0x4003f28772b0e18073b7, 0x40078f3b9a04e4a3683f),
    (0x400bcd5d5295b6b52754, 0x4007913771a24a9a9128),
    (0x400be5748c41051486a3, 0x4006abc16ee9f2ed61bc),
    (0x400692543f69e03a9288, 0x4005c596a139e3bed10f),
    (0x4006ead34ce5977bea83, 0x4004ad86fe5cd1b0ef87),
    (0x4009d9f2f6cad46c4219, 0x4006dbaeea1315daffef),
    (0x400af07e12cddf9713fe, 0x4006a54145961fcfaf1c),
]

def pld(x):
    if isinstance(x, int):
        x = x.to_bytes(10, 'little')
    a = np.empty(1, dtype=np.longdouble)
    mem = a.data.cast('B')
    mem[:10] = x
    return a[0]

def uld(x):
    a = np.empty(1, dtype=np.longdouble)
    a[0] = x
    mem = a.data.cast('B')
    return int.from_bytes(bytes(mem.tolist()[:10]), 'little')


PI = pld(0x4000c90fdaa22168c235)

def r2a(b0, b1):
    if not isinstance(b0, int):
        b0 = ord(b0)
    if not isinstance(b1, int):
        b1 = ord(b1)
    t = ((2 * PI) * b1) / 256
    return (t - np.sin(t)) * b0

def r2b(b0, b1):
    if not isinstance(b0, int):
        b0 = ord(b0)
    if not isinstance(b1, int):
        b1 = ord(b1)
    t = ((2 * PI) * b1) / 256
    return ((np.cos(t) + 1) * np.sin(t)) * b0

def brute_a(a):
    for c1 in range(ord(' '), 0x7f):
        for c2 in range(ord(' '), 0x7f):
            if np.abs(r2a(c1, c2) - a) < 1e-8:
                return bytes([c1, c2])
    return None

def brute_b(b):
    for c1 in range(ord(' '), 0x7f):
        for c2 in range(ord(' '), 0x7f):
            if np.abs(r2b(c1, c2) - b) < 1e-8:
                return bytes([c1, c2])
    return None

"""
x = a * b

y = a + b
y - a = b

x = a * (y - a)
x = a * y - a * a
a * a - y * a + x = 0

a = (y +- sqrt(y**2 - 4 * x) / 2
"""

x = pld(0)
for i in range(16):
    x = np.cos(x)
assert uld(x) == 0x3ffebd05c3a01434885a

a = r2a('z', 'e')
b = r2b('r', '0')
assert uld(a * b) == 0x400e815729fff4113f05
assert uld(a + b) == 0x4007ba7f8ca3b4f3575e

res = b''
for x, y in cons:
    x = pld(x)
    y = pld(y)
    t = np.sqrt(y ** 2 - 4 * x)
    a = (y + t) / 2
    b = y - a
    da = brute_a(a)
    db = brute_b(b)
    if da is None or db is None:
        a, b = b, a
        da = brute_a(a)
        db = brute_b(b)
    assert da is not None and db is not None
    res += da + db
res += b'}'
print(res)
