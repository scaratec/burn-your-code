# Exercise 3 — Let the critic find the bugs (13 min)

**Phase 3 of the cycle: audit the specification before any code exists.**

Defects in a specification are cheapest to fix before an agent turns them into code. In this exercise, five defects are hidden in the EquiGuard specification. An independent critic agent reads only Markdown and Gherkin and hunts them down.

## Start

Everybody loads the same specification with the hidden defects (your own files are backed up to `.workshop-backup/`):

```bash
make ex3-start
agy --model gemini-3.8-flash-high --mode auto -i "$(cat exercises/ex3-spec-critic/PROMPT.md)"
```

Start a **new** agent session — the critic must not be the author.

## What happens

The critic audits the six edges of the specification triad (BDD Guidelines §14): binding set, record vs. record, feature vs. feature, decisions vs. scenarios, limitations, and scenario honesty. It reports findings with severity and file/line on both sides.

## Done when

- [ ] You have the critic's findings table.
- [ ] You know how many of the five planted defects it found — and whether it reported anything else.

## Reference solution

`make ex3-solution` restores the defect-free specification. The five defects are revealed in the debrief.
