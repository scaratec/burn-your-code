# Title Image — "Burn Your Code"

This directory contains everything needed to (re-)generate the title image
for the talk *Burn Your Code: Feature Files as the Ultimate AI Agent Prompt*.

The image is generated photorealistically via Google's Gemini 2.5 Flash
Image model (codename *nano-banana*).

## Files

| File | Purpose |
|---|---|
| `README.md` | This file. |
| `conversation.md` | Full Q&A transcript that produced the prompt. |
| `decisions.md` | Decision matrix: every question, every alternative, chosen one marked. **This is the file to edit when iterating.** |
| `prompt.md` | The prompt that gets sent to the API. Generated from the decisions. |
| `generate.py` | Script that reads `prompt.md`, calls the API, saves PNG to `renders/`. |
| `renders/` | Output directory. Each render is timestamped. |

## Iterating on a different decision

The whole point of this directory is that you can swap any single
decision and re-generate without losing the rest of the design.

1. Open `decisions.md`.
2. Find the question you want to change (e.g. *Q11 — Brightest anchor*).
3. Change the marked option and read the "Maps to prompt section" note.
4. Edit `prompt.md` in the indicated section.
5. Re-run `python3 generate.py`.
6. Compare the new render against previous ones in `renders/`.

If you want to keep multiple variants side by side, copy `prompt.md` to
`prompt-v2.md` (or similar) and call `python3 generate.py prompt-v2.md`.

## Running

```bash
export GEMINI_API_KEY=...   # or GOOGLE_API_KEY
cd title-image
python3 generate.py
```

Output: `renders/render-YYYYMMDD-HHMMSS.png`.

Defaults: model `gemini-3-pro-image-preview` (Nano Banana Pro — premium
tier with Thinking reasoning, best text rendering), 16:9 aspect ratio,
4K output. Overrides:

```bash
GEMINI_IMAGE_MODEL=gemini-3.1-flash-image-preview \
GEMINI_IMAGE_SIZE=2K \
GEMINI_IMAGE_ASPECT=1:1 \
  python3 generate.py
```

Supported aspect ratios: `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`,
`9:16`, `16:9`, `21:9`. Supported sizes: `1K`, `2K`, `4K`.

## Cost & expectation

Each generation is a paid API call. Plan for 3–5 iterations before the
result lands. Known weaknesses of image models with this prompt:

- **Engraved Gherkin text on the mold** — keywords (`Scenario`, `Given`,
  `When`, `Then`) usually render correctly; full sentence text often
  drifts. If the wording matters exactly, plan to swap the engraving in
  Photoshop on the final pick.
- **C source code in the falling stream** — will be hallucinated. That's
  fine here because the glyphs are molten and distorting anyway.
