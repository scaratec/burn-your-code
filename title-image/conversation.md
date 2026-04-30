# Conversation Log — Title Image Prompt Construction

This is the full Q&A flow that produced `prompt.md`. Each section is
one design decision. The user's chosen option is marked **bold**.

The user's mental image at the start: *"Feature Files are a mold into which
the code is poured."* The talk title is *Burn Your Code* — anything that
doesn't fit the mold burns away.

---

## Round 1 — Foundational direction (4 questions in one batch)

### Q1 — Stylistic world

- (a) Industrial steel foundry — dark hall, sparks, glowing steel ladle into sand mold. Raw, powerful.
- **(b) Classical bronze foundry / Renaissance workshop — handcraft, dark wooden bench, bronze into a two-part clay mold.**
- (c) Precision injection mold / modern CNC form — clean, technical, controlled.

User added: *"schmutzig, düster, rauchig — es entsteht aber etwas Brilliantes."*

### Q2 — What is the mold?

- **(a) The mold IS the feature file.** Rectangular clay form, `Scenario:`, `Given`, `When`, `Then` engraved as deep negative impressions, like a typesetter's frame.
- (b) The mold is a finished product (gear, key, lock) with Gherkin engraved on the outside.

### Q3 — What is being poured?

- (a) Classic bronze — orange-glowing molten metal.
- (b) Liquid gold — radiantly bright, almost supernatural.
- **(c) Glowing bronze that forms from a stream of luminous code glyphs/ASCII** — top of the stream is still glyphs, mid-stream they fuse into metal, bottom is molten bronze filling the mold.

### Q4 — Which moment in the story?

- **(a) The act of pouring** — frozen mid-fall, transformation glyphs→bronze visible in the falling stream. Sparks, smoke, heat.
- (b) Right after — mold full, bronze pulsing orange in the Gherkin depressions, smoke rising.
- (c) The mold is opened — finished bronze piece appearing.

---

## Round 2 — Composition

### Q5 — Frame and source of the stream

- **(a) Classical source: tilting crucible/ladle from upper left.** Medium shot — heavy soot-blackened bronze pan held by chain or hand at frame edge, falling stream in mid-frame, mold lower right.
- (b) Abstract source — stream materializes from a cloud of glyphs at the top edge.
- (c) Macro — extreme close-up on the stream itself.
- (d) Wide — half-total of the entire workshop.

### Q6 — Human in the frame?

- (a) No human. Crucible tilts via chain/crane at frame edge.
- **(b) A single hand on the crucible chain — anchored at left frame edge. Anonymous.**
- (c) Half-figure of the founder, lit by the glowing stream.

**Correction by user:** *"Nicht behandschuht. grobe, starke, schmutzige Hände."* No gloves — rough, strong, dirty, calloused hands. Hand grips the chain, not the hot metal directly.

### Q7 — Engraved content of the mold

The user first asked whether `mcp-experiment` had complex scenarios — it does
not (design phase, ADRs only). They then redirected to an internal codebase, which contains a five-digit number of feature files. Three candidates were
presented:

- (b) Temporal VAT / Accounting (German, narrative) — German Corona VAT switch.
- (c) Copy Resilience / Mail Store (English, "must return NO" assertion).
- **(a) Concurrent Writes / Mail Store (English, hard "exactly 5" assertion):**

```gherkin
Scenario: 5 clients simultaneously APPEND distinct messages
          and all are stored
  Given an IMAP server with a custom storage backend running
    And 5 separate IMAP connections are authenticated
  When all 5 connections simultaneously APPEND a distinct
       message containing a 512KB attachment to the "INBOX"
  Then all 5 APPEND commands must complete with OK
   And the INBOX must contain exactly 5 messages
   And each message must be retrievable without corruption
```

Source: `services/mail-store/bdd/features/concurrent_writes.feature`.

The "exactly 5" assertion mirrors the talk's *test honesty* point. Race
condition → consistent cast also visually mirrors the foundry act.

### Q8 — Format and title space

User decision: **pure image, no title overlay, 16:9.** No reserved zone
for text. Title sits separately on the slide template.

### Q9 — Which code is being poured?

- **(a) Real implementation language of the system under test — C.** The mail-store stack in the repo (`mail-store-lib`, `cloud-storage-lib`) is C. Stream contains dense C: `pthread_create`, `cache_entry_t *entry`, `queue_push(...)`, pointer asterisks, braces.
- (b) Multiple languages in one stream (polyglot — would mirror the talk's *Language Agnosticism* slide).
- (c) Single modern readable language (Go or Python).
- (d) Stylized code-look without real syntax.

User chose authenticity over thesis-mirror: real C from the actual codebase.

---

## Round 3 — Atmosphere

### Q10 — Workshop environment

- (a) Dense workshop — many molds, second furnace, tools fully detailed.
- **(b) Reduced workshop — sooty wooden workbench, stone wall behind, distant forge glow at frame edge, tools hinted not detailed.** Clear hierarchy: form + stream are protagonists.
- (c) Black void — no background at all.

### Q11 — Where does the image burn brightest?

- (a) In the falling stream itself.
- **(b) Inside the mold, where bronze has settled into the engraved Gherkin keywords** — the keywords glow incandescent white-yellow, surrounding clay stays warm red. Visual translation of *Single Source of Truth*.
- (c) In the spark fountains at impact.
- (d) Multiple light sources, balanced.

### Q12 — Photographic style

- (a) Sebastião Salgado documentary — grainy, near-monochrome, only the glow as color.
- (b) Caravaggio chiaroscuro — near-black with dramatic spot.
- **(c) Roger Deakins cinematic** (*1917*, *Blade Runner 2049*) — anamorphic depth, soft heat shimmer, fine grain, strong but not crushed shadows.

---

## Result

All 12 decisions are consolidated in `decisions.md` and rendered into
`prompt.md`.
