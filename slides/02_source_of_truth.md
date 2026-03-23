# Single Source of Truth

The `.feature` file (Gherkin) is more than just documentation or a test.
It is the sole contract and the deterministic prompt.
Everything else is a derivative.

**No Magic Values!**
If data (like ports, IBANs, or API endpoints) is missing from the spec, the AI will hardcode it. 
The feature file must contain 100% of the runtime configuration and expected payloads. 
We enforce generic implementations through scenario variance (The "Bob-Test").
