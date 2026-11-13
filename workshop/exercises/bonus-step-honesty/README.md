# Bonus — Can the tests cheat? (for fast teams)

**Phase 4 of the cycle: audit the step definitions.**

A green test suite only means something if the step definitions are honest. Agents under pressure to "make the tests pass" produce plausible-looking step code that quietly decides the result itself. This exercise installs such a step file.

## Start

```bash
make bonus-start       # the RED state of exercise 2, but with a different step file
make test-mi1          # GREEN — although the implementation knows nothing about the fence. Suspicious?
agy --model gemini-3.8-flash-high --mode auto -i "$(cat exercises/bonus-step-honesty/PROMPT.md)"
```

## Done when

- [ ] The auditor names the lines where the step file computes or overrides the result, and the §13 check each one violates.

## Restore

`make bonus-solution` puts the honest step file back; `make test-mi1` is RED again, as it should be.
