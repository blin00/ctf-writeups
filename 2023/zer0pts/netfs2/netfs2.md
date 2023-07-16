# netfs2
misc // ptr-yudai // 2023 zer0pts ctf

## Setup
A sequel to netfs1, with some delays added if the password is incorrect.

## Solution
Consider what happens in `PyNetworkFS.authenticate` if we send a candidate password prefix, with no newline:

* If the prefix is incorrect, the server calls `timer.wait()` which waits ~5s + a random amount, sends the "Incorrect password" response, and does a random wait in `Timeout.__exit__` upon leaving the `Timeout` context.
* If the prefix is correct, the server will eventually timeout after ~5s and raise a `TimeoutError`. We leave the `Timeout` context, doing a random wait in `Timeout.__exit__`, and then the `TimeoutError` is caught and the "Incorrect password" response is sent.

After both cases, the handler exits and the connection is closed. The important difference between the cases is whether `Timeout.__exit__` and the random wait inside is run before or after sending the "Incorrect password" response.

We can distinguish these two cases by measuring the time between receiving "Incorrect password" and the connection being closed. A small delay means the prefix is correct, and a large extra delay (which should be uniformly distributed in 0-1s) means the prefix is incorrect.
In practice, the delay for a correct prefix is almost always <0.01s, so collecting one sample per character and then taking the shortest delay is reliable enough.

Logging in and reading the flag gives `zer0pts{pr0cfs_1s_5uch_4_n1c3_0r4cl3_5d17c4e}` - hmmm, we didn't need to use procfs :D
