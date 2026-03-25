# The Circular Reasoning Trap ("Testing the Test")

A critical failure in automation—especially UI testing—is re-implementing business logic within the test steps ("Glue Code").

- **The Anti-Pattern:** The test calculates the expected net amount and compares it against the UI. The test becomes "blind", validating its own potentially flawed logic.
- **The Solution:** The test step must remain "dumb". 
- **The Rule:** The truth comes 100% from the Gherkin file. The step code merely enters values and reads the resulting DOM elements or API states. We never calculate in the test code.
- **The Human Task:** Even if AI writes the steps, a human must inspect them for test honesty. LLMs tend to cheat when "green" is the success criterion.
