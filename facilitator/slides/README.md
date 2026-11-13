# Workshop slides

Offline Reveal.js deck for the 90-minute workshop (25 slides, 1920 × 1080). It sits in `facilitator/` and not in `workshop/` because slides 15, 17 and 19 reveal the reference solutions.

| | |
|---|---|
| Present | Open `index.html` in Chrome or Firefox. `F` full screen, `S` speaker view with notes, `Esc` overview. Slide 9: click the video or press `Enter` to play. |
| Fallback | `deck.pdf` (one slide per page; the video slide shows the poster) |
| Re-export the PDF | In this folder: `python3 -m http.server 8765`, then `node export-pdf.mjs http://127.0.0.1:8765/index.html deck.pdf` (Node 22+, Google Chrome). Manually: open `index.html?print-pdf` in Chrome, print with margins *None* and *Background graphics* on. |

The repository stores the video, the PDF, the fonts and the images with **Git LFS**. Without it they are only small pointer files: install Git LFS and run `git lfs pull`.

## Contents and licences

- `media/Burn-Your-Code-Autonomous-Rebuild-imap-mcp.mp4` — a 3:20 time-lapse, without sound, of a real autonomous rebuild: Gemini 3.8 Flash in the Antigravity CLI rebuilt the MCP server `imap-mcp` from its read-only specification (525 BDD scenarios, 40 ADRs, 23 LIMs), starting from zero lines of server code, until all scenarios passed twice in a row (10 h 14 min agent time). It was recorded from the agent's terminal and assembled by SCARATEC; slide 10 summarises what happened during the run, including the rule break and the finding in the generated code.
- `reveal/` — reveal.js 5.1.0, MIT licence (`reveal/LICENSE`).
- `schriften/` — Raleway, Roboto and Roboto Mono, SIL Open Font License (`OFL.txt` in each folder).
- `marke/` — SCARATEC trademarks, see `marke/README.md`.
- `media/randy.jpg` and the two badges — speaker photo and certification badges; replace them with your own when you present.
