# Single Source of Truth

The `.feature` file (Gherkin) is more than just documentation or a test.
It is the primary contract for business behavior and the most reliable prompt for the agent.
Everything else should align with it.

**No Magic Values!**
If data (like ports, IBANs, or API endpoints) is missing from the spec, the AI will hardcode it. 
The feature file must contain the business-relevant inputs, examples, and expected outputs. 
We enforce generic implementations through scenario variance (The "Bob-Test").
