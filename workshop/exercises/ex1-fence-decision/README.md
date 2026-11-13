# Exercise 1 — Decide the fence (12 min)

**Phase 1 of the cycle: decisions before code.**

A GPS point lies exactly on the fence of the pasture — on an edge or a vertex of the polygon. Inside or outside? [ADR-0001](../../governance/adr/0001-point-in-polygon-ray-casting.md) does not say, and ray casting is ambiguous there. Two correct-looking implementations can disagree. You close that gap with an architecture decision, together with the agent.

## Start

You are on track if you just ran `make check` successfully. If you lost your way: `make ex1-start`.

```bash
agy --model gemini-3.8-flash-high --mode auto -i "$(cat exercises/ex1-fence-decision/PROMPT.md)"
```

## What happens

1. The agent asks you **one question at a time**, each with options, a recommendation and the consequences: inside or outside, which numerical tolerance, GPS accuracy now or later.
2. Answer as you would for a real product. There is no wrong answer — only an unrecorded one.
3. The agent writes `governance/adr/0005-*.md` and, if you deferred something, `governance/limitations/0004-*.md`, and updates both indexes.

## Done when

- [ ] `governance/adr/0005-*.md` exists and states the rule in one sentence.
- [ ] Deferred topics are recorded in `governance/limitations/0004-*.md`.
- [ ] Both README index tables list the new records.

## Reference solution

`make ex1-solution` loads the reference decision. Exercises 2–4 build on it, so the facilitator reveals it in the debrief.
