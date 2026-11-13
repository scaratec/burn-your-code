# Facilitator guide — Burn Your Code (90-minute workshop)

Everything you need to run the workshop without its author. Participants work in `workshop/`; this directory (`facilitator/`) holds the reference solutions, the planted defects and the answer key. They live outside `workshop/` and inside a compressed archive on purpose: coding agents read files in their workspace and like to run `git show`, and plain-text solutions would end up in their context.

| Material | Path |
|---|---|
| Participant preparation (send 1–2 weeks before) | [`../workshop/PREPARATION.md`](../workshop/PREPARATION.md) |
| Exercises | [`../workshop/exercises/`](../workshop/exercises/README.md) |
| Slides (offline) and PDF fallback | [`slides/index.html`](slides/index.html), [`slides/deck.pdf`](slides/deck.pdf) |
| Answer key (reference decisions, expected results, the five defects) | `python3 facilitator/solutions.py answers` |
| Reference solutions used by the checkpoints | [`solutions.tar.gz`](solutions.tar.gz) (`solutions.py unpack` / `pack` for editing) |
| Self-check of all checkpoints | `python3 facilitator/verify_checkpoints.py` |

## 1. Before the workshop

**Two weeks before:** send `PREPARATION.md` to the participants (installation, sign-in, `make check`). Ask them to bring a charged laptop.

**On the day, at the venue:**

- [ ] Projector at 1920 × 1080 (16:9); open `facilitator/slides/index.html` in Chrome or Firefox, press `F` for full screen, `S` for the speaker view with notes.
- [ ] Play the video on slide 9 once (no sound is needed).
- [ ] `deck.pdf` on a USB stick as a fallback.
- [ ] Your own clone with **Git LFS** installed (`git lfs install` before cloning, or `git lfs pull` afterwards) — the video, the PDF and the images are LFS files.
- [ ] `make check` is green and `agy` is signed in — you demo any exercise that a participant cannot run.
- [ ] Power strips; the Wi-Fi password on a slide or flip chart.
- [ ] Optional: pair people up — one laptop with a working `agy` per pair is enough.

## 2. Run of show

| Time | Slides | What you do |
|---|---|---|
| 0:00 | 1–3 | Welcome, introduce yourself, agenda |
| 0:03 | 4–7 | Why specification-first: house of cards, 95/5, the triad, five phases and the feedback loop rule |
| 0:08 | 8–10 | Set up the video (slide 8), play it (slide 9), then be honest about the run (slide 10) |
| 0:13 | 11–12 | EquiGuard in one minute. Everybody runs `make check`; walk around and help |
| 0:16 | 13 | The question of the day: a horse on the fence |
| 0:18 | 14 | **Exercise 1** (12 min) |
| 0:30 | 15 | Debrief 1 (3 min) — reveal the reference decision |
| 0:33 | 16 | **Exercise 2** (13 min) |
| 0:46 | 17 | Debrief 2 (3 min) |
| 0:49 | 18 | **Exercise 3** (13 min) |
| 1:02 | 19 | Reveal the five defects (4 min) |
| 1:06 | 20 | **Exercise 4** (15 min); the bonus (slide 22) for fast teams |
| 1:21 | 21 | Debrief 4 (3 min) — which languages turned green? |
| 1:24 | 23–25 | Take-aways, going further, thank you |

If you fall behind: shorten exercise 2 to 10 minutes and let late teams start exercise 3 with `make ex3-start` (everybody does that anyway). Exercise 4 is the one not to cut.

## 3. The exercises

Durations below are measured dry runs with `gemini-3.8-flash-high` in a clean environment (agent time only, without reading and typing).

### Exercise 1 — Decide the fence

- **Start:** `agy --model gemini-3.8-flash-high --mode auto -i "$(cat exercises/ex1-fence-decision/PROMPT.md)"`. Participants who followed PREPARATION.md have already trusted the folder; anyone else gets "Do you trust the contents of this project?" — answer *Yes*, and if `agy` then asks before every file read, `/exit` and restart.
- **What happens:** the agent reads AGENTS.md and ADR-0001, then asks three questions, one at a time, each with options, recommendation and consequences: inside or outside, numerical tolerance, GPS accuracy now or deferred. After the third answer it writes `governance/adr/0005-*.md`, usually `governance/limitations/0004-*.md`, and updates both indexes.
- **Measured:** about 6 minutes including the three answers.
- **Watch for:** participants who answer "outside" — perfectly fine, but their exercise 2 then expects `false` on the fence. Exercise 4 starts from the reference for everybody.
- **Debrief:** both answers are legitimate if they are recorded. Reveal the reference decision (slide 15, answer key). Point out that the LIM tells the next agent what *not* to "fix".

### Exercise 2 — Make it red

- **Start:** own ADR-0005, or `make ex2-start` for the reference.
- **What happens:** new rows in Layer 1 of the error path enumeration, then one new scenario outline `@mi1 @boundary` with the vertices and edge midpoints of HomePasture plus negative controls just beyond and just inside the fence. The agent runs `make test-mi1` and explains the failures.
- **Measured:** 4–10 minutes (the slowest run spent a long time computing midpoints).
- **Expected result** with the reference decision: **24 passed, 4 failed** (which rows, and why: answer key). The old code is not wrong everywhere — it is *undecided*.
- **Debrief:** error paths first; the negative controls are what stop an implementation from cheating with a huge tolerance.

### Exercise 3 — Let the critic find the bugs

- **Start:** everybody runs `make ex3-start` (own files are backed up), then a **new** agent session with the critic prompt.
- **What happens:** the critic reads only Markdown and Gherkin and reports a findings table along the six edges of BDD Guidelines §14.3.
- **Measured:** about 4.5 minutes. In every dry run the critic found all five defects.
- **Answer key:** slide 19 and `python3 facilitator/solutions.py answers`. Ask for a show of hands: who found all five? Are other findings real contradictions or matters of taste?
- **Afterwards:** `make ex3-solution` restores the defect-free specification.

### Exercise 4 — Burn your code

- **Start:** everybody runs `make ex4-start` (deletes all application code, `make test-mi1` is RED), then the prompt with the chosen language: `sed 's/LANGUAGE/Go/g'` etc.
- **What happens:** the agent writes the CLI and a `./build.sh`, runs `make test-mi1`, fixes and repeats until the suite is green twice in a row.
- **Measured:** 2.5–6.5 minutes in Python.
- **Expected result:** **28 passed, 0 failed**; `git status` shows no change under `governance/` or `bdd/`.
- **Watch for:** compiled languages need their toolchain on the laptop; if a build fails because the compiler is missing, switch to Python. If someone's agent edited the feature file, that is the teaching moment of the day: the rule says read-only.
- **Debrief:** show of hands per language. Same specification, different code, the fence rule holds everywhere.

### Bonus — Can the tests cheat?

- `make bonus-start` loads the RED state of exercise 2 with a dishonest step file: `make test-mi1` is suddenly GREEN.
- The auditor should name the lines where the step file computes the result itself and overrides what the CLI returned (details: answer key).
- **Measured:** under 2 minutes. `make bonus-solution` restores the honest steps.

## 4. Troubleshooting

| Symptom | Fix |
|---|---|
| `agy` asks before reading every single file | The folder was trusted only in this session (PREPARATION step 3 skipped). `/exit` and start the exercise command again. |
| `agy` asks for permission before every edit or command | Auto mode is not available for this account (business/enterprise) or OS; answer `y`, or press Shift+Tab to switch to `accept-edits`. |
| `agy` says the quota is exhausted | Pair the participant with a neighbour, or use the checkpoint: `make exN-solution`. |
| Sign-in on a remote machine/WSL opens no browser | `agy` prints a URL; open it on the laptop and paste the code back. |
| `make check` fails at "MI1 test suite green" | `make workshop-start`, then `make check` again. |
| `make: command not found` on Windows | Use WSL2 (Ubuntu); the workshop does not run in plain PowerShell. |
| Someone lost their own work | Every checkpoint copies the previous files to `workshop/.workshop-backup/<time>-<checkpoint>/`. |
| The agent changed files under `governance/` or `bdd/` in exercise 4 | `git diff governance bdd` shows it; `make ex4-start` resets and the rule is a good discussion point. |
| No Wi-Fi at all | Run the exercises on your laptop as a demo; participants follow with `make exN-solution` and `make test-mi1`, which work offline once `make setup` ran. |

## 5. Maintaining the material

- The participant-facing specification is the committed state of `workshop/governance/` and `workshop/bdd/`. Checkpoints restore it with `git checkout HEAD`.
- Edit the solutions with `python3 facilitator/solutions.py unpack`, change files in `facilitator/solutions-src/` (not committed), then `python3 facilitator/solutions.py pack` and commit `solutions.tar.gz`.
- Reference solutions are overlays: `ex1/` and `ex2/` are copied on top of the committed specification; `ex4/` adds `build.sh` and `src/`. If you change the base specification, update the copies of the two README indexes in `ex1/` and the error path enumeration in `ex2/`.
- The defects of exercise 3 are text replacements in `ex3-defects.json`; each `old` text must exist in the exercise 2 reference.
- After any change: `make -C workshop setup && python3 facilitator/verify_checkpoints.py` must print nine `OK` lines.
