# Language is just a Detail

Python? Go? C? Rust?
It (almost) doesn't matter anymore.

The agent writes the code in the language we specify.
We validate the *behavior* (black box), not the syntax.

**Beyond APIs: Memory Safety & FFI**
BDD isn't limited to high-level web services. Using Foreign Function Interfaces (FFI, e.g., Python Ctypes), we load compiled C/C++ libraries (.so/.dll) directly into the BDD runner. 
The test acts as a deterministic fuzzer, mathematically proving memory safety (no segfaults) in low-level system extensions.
