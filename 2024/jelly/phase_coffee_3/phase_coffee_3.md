# phase\_coffee\_3 (the hard way)
pwn // Sheepiroo // 2024 jellyCTF // 🩸

## Setup
A pwnable that includes code to print the flag, but what if we want pop a shell instead?

checksec:
```
Arch:     amd64-64-little
RELRO:    Full RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      PIE enabled
```

No libc is provided, so I took the one from a built docker image, which matches the remote one...for now :P
The challenge binary in this repo (`./main`) has been patched to use that libc + approriate loader.

## Rev
The vuln is a stack overflow when `fgets` reads the shipping address:
```c
int BUF_SIZE = 64;
char address[BUF_SIZE];
// ...
fgets(address, 1000, stdin);
```

Stack layout, showing only relevant fields: (note: Binary Ninja's stack view doesn't correctly handle buf, which is a variable-length array)
```
-0xe8 | char buf[0x40]      // (`address` in the source, renamed to `buf` to avoid confusion)
...
-0x48 | int32_t balance_1   // to change the final balance, overwrite this, which gets copied into balance_2
...
-0x38 | void* ptr_to_buf
...
-0x1c | int32_t balance_2
...
-0x08 | saved rbp
-0x00 | saved return address
```

(To just get the flag, you can overwrite balance_1 by sending `b'A' * (0xe8 - 0x40) + p32(some_large_balance)`, and then order the flag normally.)

## Leak
The challenge echoes back the shipping address you provide, which seems like the best way to try and leak something. Unfortunately, `fgets` always adds a null terminator to the end of the input read, so we can't do the trick of smashing the stack up until right before whatever variable we want to leak. Interestingly, also on the stack is `ptr_to_buf`, which is initialized to point to `buf`. We can't leak this pointer directly, but if we modify it, then all future reads/writes to `buf` will go to the new value instead.

If we overwrite just the lowest byte of `ptr_to_buf` with a null byte (the one `fgets` adds), then it'll point some random number of bytes lower on the stack, depending on what the initial random stack offset was, which will leak...something. (The stack needs to be 16 byte aligned, so there's only 256 / 16 = 16 possible values for this byte.) Looking at the resulting corrupted shipping address that's sent back, the possible leaks are:

1. main+0x2148
2. libc+0x2038e0
3. various stack addresses
4. garbage (contents of `buf`, small constants)

Note that if we want to do this leak more than once, now that `ptr_to_buf` points lower on the stack, doing a similar overflow again will overwrite the saved return address of `fgets` or similar and crash before getting back to `main` if you're not careful.

## Pwn
The libc leak is the most useful - it occurs with the minimal probability of 1/16, so we need to retry until we get it. There's no stack canary, so we can just overwrite a saved return address on the stack to get code exec and and start whatever ROP payload we want.

For the final payload, I decided to use `one_gadget` + a bit of ROP beforehand to set up some required registers.

Flag (in `flag.txt`): `jellyCTF{ph4se_c0nn3ct_15_definitely_a_coff33_comp4ny}`
