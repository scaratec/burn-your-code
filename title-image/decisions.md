# Decision Matrix

Every design decision for the title image. The chosen option is
**bold**. To iterate, change a choice here, edit the matching section
in `prompt.md`, then re-run `generate.py`.

---

## Q1 — Stylistic world

| Option | Description | Chosen |
|---|---|:---:|
| 1a | Industrial steel foundry — dark hall, sparks, glowing steel ladle, sand mold. | |
| **1b** | **Classical bronze foundry / Renaissance workshop — handcraft, wooden bench, two-part clay mold. Dirty, dark, smoky, but something brilliant emerges.** | ✓ |
| 1c | Precision injection mold / modern CNC — clean, technical, controlled. | |

**Maps to:** `prompt.md` → `SETTING` paragraph + overall tone.

---

## Q2 — What IS the mold?

| Option | Description | Chosen |
|---|---|:---:|
| **2a** | **The mold IS the feature file. Rectangular clay slab with `Scenario:`, `Given`, `When`, `Then` engraved as deep negative impressions, like a typesetter's frame.** | ✓ |
| 2b | The mold is a finished product (gear, key, lock); Gherkin engraved on the outside. | |

**Maps to:** `prompt.md` → mold description block ("Lower right: a rectangular clay casting mold...").

---

## Q3 — What is being poured?

| Option | Description | Chosen |
|---|---|:---:|
| 3a | Classic glowing bronze. Earthy, honest. | |
| 3b | Liquid gold — radiantly bright, supernatural. | |
| **3c** | **Stream of luminous code glyphs that fuses mid-fall into bronze. Top: glyphs. Middle: distorting/melting. Bottom: molten metal.** | ✓ |

**Maps to:** `prompt.md` → "Center vertical axis: the pour" block.

---

## Q4 — Which moment in the story?

| Option | Description | Chosen |
|---|---|:---:|
| **4a** | **The act of pouring — frozen mid-fall. Transformation visible in the stream. Sparks, smoke, heat.** | ✓ |
| 4b | Right after — mold full, bronze pulsing orange in the depressions, smoke rising. | |
| 4c | Mold is opened — finished bronze piece revealed. | |

**Maps to:** `prompt.md` → entire composition (the pour is the central action).

---

## Q5 — Frame and source of the stream

| Option | Description | Chosen |
|---|---|:---:|
| **5a** | **Classical: tilting crucible upper left, stream center, mold lower right. Medium shot.** | ✓ |
| 5b | Abstract: stream materializes from a cloud of glyphs at the top edge — no crucible. | |
| 5c | Macro: extreme close-up on the stream itself. | |
| 5d | Wide: half-total of the workshop. | |

**Maps to:** `prompt.md` → "COMPOSITION (medium shot)" block, three sub-sections.

---

## Q6 — Human in the frame?

| Option | Description | Chosen |
|---|---|:---:|
| 6a | No human at all. Chain or crane tilts the crucible. | |
| **6b** | **A single hand at the crucible chain — anchored at left frame edge. Anonymous. *Bare, rough, strong, dirty, calloused.* No gloves. Hand on the chain, not on the hot metal.** | ✓ |
| 6c | Half-figure of the founder, lit by the glowing stream. | |

**Maps to:** `prompt.md` → "Upper left:" block.

---

## Q7 — Engraved Gherkin content

Source candidates for engraved scenario text on the mold (after rejecting `mcp-experiment` — design phase only — and EquiGuard from the talk's own workshop):

| Option | Source | Chosen |
|---|---|:---:|
| **7a** | **`acme/repo/services/mail-store/bdd/features/concurrent_writes.feature` — "5 clients APPEND" scenario. English. Hard `exactly 5` assertion mirrors test-honesty thesis.** | ✓ |
| 7b | `acme/repo/services/billing/features/use_cases/billing_temporal_vat.feature` — German, narrative, with data tables. | |
| 7c | `acme/repo/services/mail-store/bdd/features/copy_resilience.feature` — English, negative test ("returns NO"). | |

The chosen scenario, as engraved on the mold:

```gherkin
Scenario: 5 clients simultaneously APPEND
          distinct messages and all are stored
  Given an IMAP server with a custom storage backend
    And 5 IMAP connections authenticated
  When all 5 connections APPEND a distinct
       512KB attachment to the "INBOX"
  Then all 5 APPENDs return OK
   And the INBOX contains exactly 5 messages
```

(Slightly compressed from the original to fit a clay mold and stay legible at 16:9.)

**Maps to:** `prompt.md` → engraved-text block inside mold description.

---

## Q8 — Format and title space

| Option | Description | Chosen |
|---|---|:---:|
| 8a | 16:9 with a quiet zone for an overlaid title "Burn Your Code". | |
| **8b** | **16:9, pure image, no title in the frame.** | ✓ |
| 8c | Additional 1:1 render for social/CFP. | |

**Maps to:** prompt opening line + `NEGATIVE` directives.

---

## Q9 — Which code is in the falling stream?

| Option | Description | Chosen |
|---|---|:---:|
| **9a** | **Real C source code matching the system-under-test. Tokens like `pthread_create`, `cache_entry_t *entry`, `queue_push(...)`, pointer asterisks, braces.** | ✓ |
| 9b | Multiple languages (polyglot stream — would mirror the *Language Agnosticism* slide). | |
| 9c | Single modern readable language (Go or Python). | |
| 9d | Stylized code-look without real syntax. | |

**Maps to:** `prompt.md` → "Center vertical axis: the pour" / TOP-of-stream description.

---

## Q10 — Workshop environment

| Option | Description | Chosen |
|---|---|:---:|
| 10a | Dense workshop — multiple molds, second furnace, tools fully detailed. | |
| **10b** | **Reduced workshop — sooty wooden workbench, stone wall, distant forge glow at frame edge, tools only hinted.** | ✓ |
| 10c | Black void — no background at all. | |

**Maps to:** `prompt.md` → `SETTING` paragraph.

---

## Q11 — Where does the image burn brightest?

| Option | Description | Chosen |
|---|---|:---:|
| 11a | In the falling stream itself. | |
| **11b** | **Inside the mold — bronze pooling in the engraved Gherkin keywords, glowing incandescent white-yellow. Visual translation of "Single Source of Truth".** | ✓ |
| 11c | In the spark fountains at impact. | |
| 11d | Multiple light sources, balanced. | |

**Maps to:** `prompt.md` → `LIGHTING HIERARCHY` block.

---

## Q12 — Photographic style

| Option | Description | Chosen |
|---|---|:---:|
| 12a | Sebastião Salgado documentary — grainy, near-monochrome, only the glow as color. | |
| 12b | Caravaggio chiaroscuro — near-black with dramatic spot. | |
| **12c** | **Roger Deakins cinematic (*1917*, *Blade Runner 2049*) — anamorphic depth, soft heat shimmer, fine grain, strong but not crushed shadows.** | ✓ |

**Maps to:** `prompt.md` → opening style line + atmosphere block.

---

## Round 4 — v2 revisions after first render

After viewing `renders/render-20260426-212107.png` (v1), the user
identified four problems and revised the geometry. v2 lives in
`prompt-v2.md`; v1 (`prompt.md`) is preserved unchanged for comparison.

### Q2 (revised) — What IS the form?

| Option | Description | v1 | v2 |
|---|---|:---:|:---:|
| 2a | Flat clay slab, Gherkin engraved as **internal** negative-relief depressions. The keywords get filled with bronze. | ✓ | |
| **2b'** (new) | **Thick hand-thrown ceramic vessel (bulbous wide-mouthed clay pot, soup-tureen sized). Gherkin engraved as **external** raised relief on the outer wall. Pot interior is unmarked.** | | ✓ |

**Why changed:** "Es macht keinen Sinn, die Buchstaben auszugießen." The
spec is what's *visible* on the outside; the code becomes the substance
*inside*. The previous "fill the keyword cavities with bronze" idea
conflated the two layers.

### Q5 (revised) — Composition

| Aspect | v1 | v2 |
|---|---|---|
| Crucible position | Upper-left, tilted | **Centre-upper, directly above pot** |
| Stream width | Thin/medium | **Wide, thick (forearm-breadth)** |
| Mold position | Lower-right | **Centre-foreground (the dominant object)** |
| Hand position | Left edge, on chain | Left edge, on **tilting chain** (separate from the lifting mechanism) |

**Why changed:** "Der Tiegel muss also auch wesentlich mehr im Mittelpunkt
stehen." Stream width is dictated by Q9's revision: glyphs need to be
visibly inside the stream, so the stream must be wide.

### Q9 (revised) — Code in the stream

| Option | Description | v1 | v2 |
|---|---|:---:|:---:|
| 9a | Real C source code. (Unchanged in spirit.) | ✓ | ✓ |
| **9a'** (clarified) | **C glyphs live STRICTLY INSIDE the molten stream as embedded characters. NOT as a side caption, NOT as an overlay, NOT as floating text. Each character is large enough to read inside the flow.** | | ✓ |

**Why changed:** v1 rendered the code as a text caption beside the stream,
not inside it — losing the talk's central transformation metaphor.

### Q11 (revised) — Brightest anchor

| Option | Description | v1 | v2 |
|---|---|:---:|:---:|
| 11b | Inside the mold, where bronze fills the engraved Gherkin keywords (incandescent white-yellow). | ✓ | |
| **11b'** (new) | **The engraved Gherkin text on the outer wall of the pot, lit from above by the falling stream and from within by the rising molten bronze level. Keywords (Scenario / Given / When / Then) glow warm gold against the sooty clay.** | | ✓ |

**Why changed:** Q2 revision invalidated the old anchor. New thematic
read: the spec is *illuminated from inside* by the substance that fills
it — visible truth backlit by implementation.

### Q7 (revised) — Engraved Gherkin content (richer technical detail)

User requested more technical density in the engraving. v1/v2 used a
compressed paraphrase; the revised version stays close to the original
feature file and preserves real config flags, mock-server detail, and
the FETCH-corruption verification step. The engraved text now reads:

```gherkin
@security @concurrent
Feature: Concurrent Write Safety

  Scenario: 5 clients simultaneously APPEND distinct
            messages and all are stored
    Given an IMAP server with a custom storage backend
      And attachment_threshold_bytes = 1 byte
      And a Storage Mock Server accepting concurrent uploads
      And 5 IMAP connections authenticated
    When all 5 connections simultaneously APPEND
         a distinct message containing a 512KB
         attachment to the "INBOX"
    Then all 5 APPEND commands must complete OK
     And the INBOX must contain exactly 5 messages
     And each message must be retrievable via FETCH
         without corruption
```

**Why changed:** "Ich möchte auch mehr technische Details in dem Gherkin
sehen." Adds: `@security @concurrent` tags, `Feature:` header, explicit
`attachment_threshold_bytes = 1 byte` config, Storage Mock Server, FETCH
without corruption — all from the original `concurrent_writes.feature`.

### Q9 (re-emphasised) — Code only inside the flowing mass

The negative section in v2 was strengthened with absolute language: NO
C source code visible anywhere outside the falling molten stream, NO
captions / labels / annotations / HUD / subtitles / sticky notes / panels.
Every single C glyph must live inside the molten flow.

**Why changed:** "Den code soll man auf jeden Fall sehen aber, wirklich
nur in der flüssigen Masse beim Rausgießen." Reinforces the v2 intent
because v1 rendered the code as a side caption — the model needs harder
prohibition language.

### Unchanged (after v2)

Q1 (Renaissance bronze foundry, dirty, brilliant outcome), Q3 (stream of
code glyphs transforming into bronze), Q4 (act of pouring, frozen), Q6
(bare dirty hand on chain, no glove), Q8 (16:9, no overlay title), Q10
(reduced workshop), Q12 (Roger Deakins style).

---

## Round 5 — v3 revisions after second render

After viewing `renders/render-20260426-213751.png` (v2), the user
identified four further problems and pivoted the aesthetic toward Lord
of the Rings. v3 lives in `prompt-v3.md`; v2 is preserved unchanged.

### Q1 (revised) — Stylistic world

| Option | Description | v1/v2 | v3 |
|---|---|:---:|:---:|
| 1b | Renaissance bronze foundry — handcraft, wooden bench, two-part clay mold. | ✓ | |
| **1b''** (new) | **Mythic ancient forge — Mount Doom / Khazad-dûm aesthetic, dwarven smithy under the mountain. Same casting craft, but with mythic weight and primordial ritual atmosphere.** | | ✓ |

**Why changed:** "Ich habe da mehr so die Stimmung aus Herr der Ringe im
Kopf." Renaissance workshop reads too clean / domestic; LOTR forge reads
sacred and dangerous, which carries the talk's "casting code as ritual"
better.

### Q2 (revised again) — Vessel material and form

| Option | Description | v2 | v3 |
|---|---|:---:|:---:|
| 2b' | Refined hand-thrown ceramic vessel, soup-tureen sized, with external Gherkin engraving. | ✓ | |
| **2b''** (new) | **Primitive forge cauldron: charcoal-black hand-fired clay, almost obsidian in tone, raw soot encrustation, deep scorching, visible cracks, irregular hand-hewn surface, bound by dark iron strapping with rusted rivets. Dwarven, ritual, weighty.** | | ✓ |

**Why changed:** "Die Form sieht noch total gerendert aus. Die kann ruhig
noch schwärzer und gröber sein." v2 vessel read as kitchenware; v3 reads
as ancient ritual cauldron.

### Q5 (revised again) — Camera perspective

| Aspect | v1/v2 | v3 |
|---|---|---|
| Camera angle | Frontal, centred | **Three-quarter view, ~30° off frontal axis, slightly above eye level looking down** |
| Vessel orientation | Flat to camera | **Turned, showing curvature; inscription wraps around the body** |

**Why changed:** "Die Perspektive gefällt mir noch nicht. Das ist jetzt
alles so ausgerichtet, dass man den Text gut lesen kann." Frontal
composition reads as documentation diagram; 3/4 reads as cinematic
moment.

### Q7 (revised emphasis) — Inscription readability

| Aspect | v2 | v3 |
|---|---|---|
| Engraving style | Raised relief, painted/branded look in render | **Genuinely 3D-chiselled raised relief, hard shadows inside each letterform** |
| Readability target | Fully readable to viewer | **Front-facing portion clearly recognisable; wrapped/shadowed side intentionally illegible** |

**Why changed:** "Es reicht ja, wenn man Teile davon erkennen kann." User
explicitly accepts partial readability — favouring authenticity of relief
over completeness of text.

### Q12 (revised) — Photographic style

| Option | Description | v1/v2 | v3 |
|---|---|:---:|:---:|
| 12c | Roger Deakins cinematic. | ✓ | |
| **12c'** (new) | **Roger Deakins chiaroscuro fused with Andrew Lesnie's LOTR cinematography — heavy volumetric haze, sharp warm god-rays through smoke, crushed cool grey-green shadows against saturated warm-orange highlights, mythic weight.** | | ✓ |

**Why changed:** Same direction as Q1 — the cinematographic vocabulary
follows the world shift to LOTR-mythic.

### Unchanged (after v3)

Q3 (code glyphs transforming into bronze inside the stream), Q4 (act of
pouring), Q6 (bare dirty hand on left edge), Q7 text content (same
concurrent_writes scenario), Q8 (16:9, no overlay title), Q9 (real C, in
stream only), Q10 (reduced workshop — pushed even further into shadow),
Q11 (inscription is the bright anchor, now via raised-relief shadow play
instead of bronze-fill).

---

## Round 6 — v4 structural fixes after third render

After viewing `renders/render-20260426-221636.png` (v3), three model
defaults persisted despite explicit negation: code as side caption,
inscription as painted glow, cauldron not black enough. v4 attacks all
three structurally rather than by negation. v3 is preserved unchanged
in `prompt-v3.md`.

### Structural shift 1 — Critical-constraints block at top

The two hardest constraints (code-as-relief, intaglio inscription) are
hoisted to the very top of the prompt as numbered CRITICAL CONSTRAINTS,
before atmosphere/setting description. Image models attend most
strongly to the opening of a prompt; relegating these to the negative
section at the end was demonstrably insufficient.

### Q2 (revised again) — Cauldron material

| Option | Description | v2 | v3 | v4 |
|---|---|:---:|:---:|:---:|
| 2b' | Refined hand-thrown ceramic vessel. | ✓ | | |
| 2b'' | Charcoal-black hand-fired clay, soot-encrusted, with iron banding. | | ✓ | |
| **2b'''** (new) | **Hand-forged BLACK IRON cauldron — wrought iron plates joined by deep-driven rivets, hammer-marked surface, oxidised patina, iron carrying rings, dwarven-forge weight. NOT clay, NOT ceramic.** | | | ✓ |

**Why changed:** v3 still rendered the cauldron as warm-brown patina
ceramic. Switching the material from clay to iron solves the colour
problem structurally — iron is naturally near-black — and matches the
LOTR/dwarven aesthetic better than fired clay ever could.

### Q9 (revised again) — Code in the stream as sculpted relief

| Option | Description | v2 | v3 | v4 |
|---|---|:---:|:---:|:---:|
| 9a | C glyphs embedded inside the molten flow. | ✓ | ✓ | |
| **9a'** (new) | **C code as 3D RELIEF sculpted FROM the stream's own surface — same material, same heat, same colour as the stream itself; visible only via ridge-light on raised edges and recess-shadow between extrusions. Not embedded glyphs in molten matter — the molten matter IS the code.** | | | ✓ |

**Why changed:** v3 still partially rendered code as floating
side-captions despite explicit negation. Re-framing the code as
geometrically inseparable from the flow's own surface removes the
model's option to render it as text. Code can no longer be detached
because it is the surface itself.

### Q11 (revised again) — Inscription rendering: intaglio not relief

| Option | Description | v2 | v3 | v4 |
|---|---|:---:|:---:|:---:|
| 11b' | Engraved Gherkin in raised relief on outer wall, lit from above and within, glowing warm gold. | ✓ | ✓ | |
| **11b''** (new) | **Inscription CHISELED INTO the iron as INTAGLIO — sunken negative-space cuts. Letters do NOT glow, are NOT self-luminous, and are visible ONLY via shadow inside their carved channels and warm rim-light raking across the iron surface.** | | | ✓ |

**Why changed:** Both v2 and v3 rendered the inscription as painted
warm-glow text on the vessel surface, not as 3D relief. The fix is to
flip the geometry from raised (which the model paints over) to sunken
intaglio (which has no surface to paint — only shadow inside cuts).

### Unchanged (after v4)

Q1 (LOTR-mythic foundry), Q3 (code stream transforming into bronze),
Q4 (act of pouring), Q5 (3/4 view, ~30° off frontal), Q6 (bare dirty
hand on left edge), Q7 text content, Q8 (16:9, no overlay title), Q10
(reduced background), Q12 (LOTR + Deakins).

