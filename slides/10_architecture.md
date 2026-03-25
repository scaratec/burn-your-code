# Language is just a Detail

Python? Go? C? Rust?
For many problem domains, it matters less at the start than teams assume.

The agent writes the code in the language we specify.
We validate the *behavior* (black box), not the syntax.

**Beyond APIs: Memory Safety & FFI**
BDD isn't limited to high-level web services. Using Foreign Function Interfaces (FFI, e.g., Python Ctypes), we load compiled C/C++ libraries (.so/.dll) directly into the BDD runner. 
The test can act as a deterministic stress harness, giving us empirical evidence that low-level system extensions behave safely under the covered scenarios.
