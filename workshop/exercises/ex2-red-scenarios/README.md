# Exercise 2 — Make it red (13 min)

**Phase 2 of the cycle: error paths first, then scenarios — RED.**

Your decision from exercise 1 becomes executable. First the agent enumerates the new error paths, then it writes the scenarios. The test suite turns **red**: the current implementation knows nothing about the fence yet. That is exactly the point.

## Start

Continue with your own ADR-0005 from exercise 1, or load the reference: `make ex2-start`.

```bash
agy --model gemini-3.8-flash-high --mode auto -i "$(cat exercises/ex2-red-scenarios/PROMPT.md)"
```

## What happens

1. New rows in Layer 1 of `bdd/00_error_path_enumeration.md`: on a vertex, on an edge, just beyond and just inside the fence — and anything you deferred.
2. One new `Scenario Outline` in `bdd/mi1_geofence_library.feature` with the vertices and edge midpoints of `HomePasture`, points just within and just beyond the numerical tolerance, and negative controls 0.1 m away from the fence.
3. The agent runs `make test-mi1`.

## Done when

- [ ] Every new error path row is `exec` with a scenario row, or `none` with a reason.
- [ ] `make test-mi1` is **RED**: some boundary rows fail, the 16 existing scenarios still pass.
- [ ] You can say why each failing row fails.

## Reference solution

`make ex2-solution` — 16 boundary rows; `make test-mi1` reports 26 passed and 6 failed.
