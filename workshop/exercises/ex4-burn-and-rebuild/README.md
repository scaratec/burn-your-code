# Exercise 4 — Burn your code (15 min)

**Phase 5 of the cycle: the specification is complete, the code is a disposable artifact.**

All application code is deleted. What remains is the specification: decisions, limitations, error paths, scenarios and black-box steps. You choose any programming language, and the agent rebuilds the geofence library from the specification alone — including your rule for the fence.

## Start

Everybody starts from the clean specification with the boundary scenarios (your files are backed up):

```bash
make ex4-start
make test-mi1          # RED: there is no implementation at all
```

Pick a language whose toolchain is installed on your laptop. **Python always works** (the tests need it anyway); Go, TypeScript/Node.js, Rust or Java if you have them.

```bash
agy --model gemini-3.8-flash-high --mode auto -i "$(sed 's/LANGUAGE/Python/g' exercises/ex4-burn-and-rebuild/PROMPT.md)"
```

Replace `Python` with your language.

## What happens

The agent writes the CLI and a `./build.sh`, runs `make test-mi1`, fixes, and repeats until everything is green twice in a row. It must not touch `governance/` or `bdd/`.

## Done when

- [ ] `make test-mi1` is **GREEN** with 28 scenarios passed, 0 failed.
- [ ] `git status` shows no change under `governance/` or `bdd/`.

## Reference solution

`make ex4-solution` loads a reference implementation in Python.
