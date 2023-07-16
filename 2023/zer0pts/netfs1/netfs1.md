# netfs1
misc // ptr-yudai // 2023 zer0pts ctf

## Setup
We're given the source for a file viewer written in Python. The flag is stored at the path `secret/flag.txt`, but the catch is that only the `admin` user is allowed to view paths that contain the literal string `secret`.

## Solution
The password check is:

```python
# Receive password
self.response(b"Password: ")
i = 0
while i < len(password):
    c = self._conn.recv(1)
    if c == b'':
        return
    elif c != password[i:i+1]:
        self.response(b"Incorrect password.\n")
        return
    i += 1
```

which compares the input one byte at a time against the correct password, failing immediately upon reaching an incorrect character.
This means we can query whether some string is a prefix of the password by sending it as the password, without a newline.
If it's incorrect, we'll immediately receive the "Incorrect password" response.
If it's correct, the server will continue reading input, and there'll be no response until the timeout is reached.

By trying `(current known prefix) + (new candidate character)` for all possible candidate characters, we can incrementally bruteforce the entire password.

Once we know the admin password, we can simply login as admin and read the flag: `zer0pts{d0Nt_r3sp0nd_t00_qu1ck}`.
