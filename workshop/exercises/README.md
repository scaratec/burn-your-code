# Burn Your Code — 90-minute hands-on workshop

One story, four exercises: **what happens when a horse stands exactly on the fence?**

EquiGuard decides whether a GPS ping from a horse collar lies inside its pasture. The specification does not say what happens on the fence line itself. You close that gap the specification-first way — decide, specify, audit, and let the agent rebuild the code in a language of your choice:

| # | Exercise | Phase of the cycle | Time | Result |
|---|---|---|---|---|
| 1 | [Decide the fence](ex1-fence-decision/README.md) | Decisions (ADR, LIM) | 12 min | ADR-0005, LIM-0004 |
| 2 | [Make it red](ex2-red-scenarios/README.md) | Error paths & feature file | 13 min | boundary scenarios, suite **RED** |
| 3 | [Let the critic find the bugs](ex3-spec-critic/README.md) | Specification critic | 13 min | findings for 5 hidden defects |
| 4 | [Burn your code](ex4-burn-and-rebuild/README.md) | Autonomous implementation | 15 min | any language, suite **GREEN** |
| + | [Can the tests cheat?](bonus-step-honesty/README.md) | Step honesty audit | bonus | for fast teams |

## Before you start

Follow [`../PREPARATION.md`](../PREPARATION.md) at home and finish with:

```bash
cd burn-your-code/workshop
make check
```

All exercises run locally: Python, the Antigravity CLI (`agy`) and the model **Gemini 3.8 Flash (High)**. No Docker, no cloud account.

## Rules of the game

- Run every command from the `workshop/` directory.
- Paste nothing by hand: each exercise starts with one `agy ... -i "$(cat .../PROMPT.md)"` command. `--mode auto` lets the agent edit files and run safe commands without asking; where auto mode is not available, `agy` asks — answer `y`.
- If `agy` asks before reading every single file, the folder was trusted only in this session: `/exit` and start the command again.
- Fell behind? Every exercise has `make exN-start` (jump in) and `make exN-solution` (reference). Your own files are copied to `.workshop-backup/` before anything is overwritten.
- The feedback loop rule: whatever the critic or reality finds changes the **ADR, LIM or feature file first** — never the code directly.

## Agenda

| Time | Block |
|---|---|
| 0:00 | Welcome, speaker, why specification-first (95/5) |
| 0:08 | Video: one prompt, a complete MCP server |
| 0:13 | EquiGuard and the specification triad, `make check` |
| 0:18 | Exercise 1 + debrief |
| 0:33 | Exercise 2 + debrief |
| 0:49 | Exercise 3 + reveal of the five defects |
| 1:06 | Exercise 4 + debrief: which languages turned green? |
| 1:24 | Wrap-up and next steps |
