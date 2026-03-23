# The Myth of the One-Shot Generation

**FAQ: "What if a human manually changes the code?"**

**1. It is highly iterative (Not a One-Shot)**
We don't generate the whole app at once. We write *one* scenario, the agent implements it (Red -> Green). We write the *next* scenario, the agent extends the code. It is a continuous, granular evolution.

**2. The Manual Change Trap**
If a developer manually changes the implementation code (`.go`, `.py`, `.java`) without updating the `.feature` file, they create technical debt immediately. 

**3. The Golden Rule**
If a behavior isn't documented in the feature file, it doesn't exist. The agent might overwrite your manual "hotfix" during the next refactoring cycle because it isn't protected by a test. 
**To change the code, you must change the spec.**