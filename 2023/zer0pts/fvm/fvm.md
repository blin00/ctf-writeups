# fvm
rev // ptr-yudai // 2023 zer0pts ctf

## Setup
Flavortext: "Are you bored with x86? Enjoy this x87 VM."

We're given just a binary, which is a flag checker.

## Reversing the VM
The flavortext doesn't lie: there's a big blob of bytecode that gets passed into `fvm::emulate()`, which is a pretty standard instruction dispatch loop, with a giant `switch` jump table to handle each instruction. As promised, most of the operations are x87 instructions :).

It's more tedious than anything else figuring out what each opcode does and hacking together a quick disassembler (`disas.py`). In short:
* all instructions start with a 1-byte opcode
* some instructions are followed by a 2-byte relative jump offset
* one instruction, which pushes a constant onto the x87 stack, is followed by that 10 byte immediate (remember that x87 registers are 80 bits wide)

## Reversing the Bytecode
Luckily, looking a simple linear disassembly (`code.s`) is enough - there's never any jumps into the middle of an instruction, for example.

The flag checking routine, in pseudocode, looks like:

```
print("FLAG: ");
accumulator = 0;

c0 = getchar(), c1 = getchar(), c2 = getchar(), c3 = getchar();
if (c0, c1, c2, c3 are not in range [0x20, 0x7f)) goto fail;
a = (2 * pi * c1 / 256 - sin(2 * pi * c1 / 256)) * c0;
b = (cos(2 * pi * c3 / 256) + 1) * sin(2 * pi * c3 / 256) * c2;
if (a * b == constant1) accumulator = cos(accumulator);
if (a + b == constant2) accumulator = cos(accumulator);

(repeat above block 7 more times, with different constants)

if (getchar() != '}') goto fail;
// following constant is cos iterated 16 times on 0
if (accumulator != 0x3ffebd05c3a01434885a) goto fail;

goto success;
```

For each block, we can determine the values of `a` and `b`, but not their order, by solving the quadratic obtained from substituting `b = constant2 - a` into `a * b = constant1`. Then we can check all `95 * 95 = 9025` possible pairs of input characters and see which gives the correct values for `a` and `b`. This is implemented in `solve.py`.

The final flag is `zer0pts{fun_0f_FPU_st4ck_m4ch1n3}`.
