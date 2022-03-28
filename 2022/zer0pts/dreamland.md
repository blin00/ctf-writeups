# dreamland
rev // ptr-yudai // 2022 zer0pts ctf

## Setup
We're given an encrypted flag and the binary used to encrypt it: the goal is to figure out how the flag encryptor works and then decrypt the flag.

## Obfuscation
The primary obfuscation in the encryptor binary is using `setjmp`/`longjmp` for iteration: constructs like
```c
for (int ctr = 0; ctr < 100; ctr++) {
    do_something();
}
```

are sometimes implemented as the following:
```c
jmp_buf state;
int ctr = setjmp(state);
if (ctr < 100) {
    do_something();
    longjmp(state, ctr + 1);
}
```

These loop constructs can also be nested. Thankfully, the `state` is only used in `setjmp`/`longjmp` calls and is never read or modified directly.

Both Ghidra and Binary Ninja's decompilers were confused enough to incorrectly assign constant values to several variables - for example, that the return value of `create_dream` is always `0`.

## Encryptor
The encryptor (which has symbols intact, yay) implements a stream cipher:

1. Checks that the flag is ASCII
2. Generates 18 random bytes, 15 of which are used to initialize a 200-bit state vector by `initialize_dream`
3. Encrypts the flag by XORing each byte with a byte from the keystream (returned by `create_dream`), and writes the encrypted flag to the output
4. Writes the resulting 200-bit state vector to the output

The 200-bit state is split into two 100-bit parts. `__nightmare` does most of the grunt work of the cipher: it calculates some bits that are dependent on both halves of the state, and then calls `__nightmare_r` on the first half and `__nightmare_s` on the second half.

## Solution
The final state of the stream cipher is in the encrypted flag file, so ideally we'd like to run the stream cipher backwards from that state to recover the keystream. The state transition function is not linear, so it can't be trivially inverted. However, we know the plaintext must be ASCII, which it turns out is a strong enough constraint to let us recover the flag, without needing to analyze the cipher itself.

The solution code:
* Begins with the set of goal states as just the given final state
* Uses z3 to solve for all previous states such that
    - advancing the stream cipher one byte leads to some goal state
    - (generated keystream byte XOR ciphertext byte) is ASCII (as a simplification, only enforces that the most significant bit is unset)
* Let the goal state set be the set of previous states we just solved for, and repeat

It turns out at every step there at most ~35 possible candidate states, which is very tractable. The final computed flag is unique excluding the first byte, and knowing the flag starts with `zer0pts{`, it must be `zer0pts{Mu7u4l_1rr3gul4r_Cl0ck1ng_KEYstr34m_g3n3r470r}`.
