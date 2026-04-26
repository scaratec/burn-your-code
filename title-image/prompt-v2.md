# Prompt v2 — vessel-centred restructure

Iteration after v1 render. Same talk, same scenario, different geometry:
the receiving form is now a thick ceramic vessel with Gherkin engraved on
the OUTSIDE wall; the C code lives strictly INSIDE the falling stream,
which is now wide enough to carry readable glyphs.

```
Photorealistic cinematic frame, 16:9 anamorphic widescreen, in the visual
style of Roger Deakins (1917, Blade Runner 2049): shallow depth of field,
soft volumetric haze, dense drifting smoke, strong heat shimmer, fine
natural film grain, deliberate light hierarchy with deep but not crushed
shadows.

SETTING — A small Renaissance-era bronze foundry, late at night. The air
is thick with soot and drifting smoke, especially in the upper third of
frame. The dim red ambient glow of a distant forge sits at the far right
edge. A weathered, ash-blackened heavy oak workbench dominates the lower
portion. The stone wall behind is rough and scorched, lit only
indirectly. A few iron tools — tongs, a long skimmer — hang in soft
focus on the wall, suggested rather than detailed.

COMPOSITION (medium shot, vessel-centred, vertical axis through the
middle of the frame) —

Crucible: centred horizontally, positioned in the upper third of frame,
heavy, soot-blackened, bronze, suspended from above by an iron support
mechanism (largely off-frame at the top). The crucible is tilted forward,
pouring directly downward into the vessel below. A separate iron tilting
chain runs from the side handle of the crucible diagonally down to the
left frame edge.

Hand on tilting chain: at the left frame edge, a single bare human
hand — large, calloused, knuckles black with carbon dust, dirt under the
fingernails, weathered skin, NO glove — grips the tilting chain firmly.
Only the hand and a sliver of forearm are visible at the very edge.

The pour (centre vertical axis, the action core of the image): a WIDE,
THICK column of molten matter — roughly the breadth of an adult's
forearm — falls from the crucible mouth straight down into the open
mouth of the vessel. The column is dense, viscous, glowing. Embedded
THROUGHOUT the falling mass — NOT beside it, NOT above it as a caption,
NOT as floating overlay text — are large, luminous C source code glyphs.
Clearly readable tokens float and tumble inside the molten flow itself:
pthread_create, cache_entry_t *entry, queue_push(ctx, "INBOX", ...),
pointer asterisks, braces, semicolons, struct declarations. The glyphs
are LARGE — each character occupies roughly the height of a thumbnail at
this scale — and unmistakably part of the flowing material. White-hot
yellow at the top of the stream where glyphs are intact; softening and
smearing into incandescent orange in the middle as glyphs deform; pure
molten bronze with no remaining glyphs at the bottom as the flow enters
the vessel.

The vessel (centre-foreground, lower-mid frame): a thick, heavy, ancient
hand-thrown ceramic vessel — a wide-mouthed bulbous clay pot, the size
of a large soup tureen, planted firmly on the workbench. Walls are
thick, with visible clay grain, pitting, hand-thrown imperfections,
scorched and soot-streaked from past use. The mouth is open and round,
receiving the pour. On the OUTER wall of the pot, facing the camera,
deeply engraved Gherkin text in raised relief reads exactly, line by
line:

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

The engraving is LARGE, deep, hand-cut, clearly readable to the viewer.
The keywords @security, @concurrent, Feature, Scenario, Given, When,
Then are noticeably bolder than the surrounding text. The technical
tokens (attachment_threshold_bytes, GCS, IMAP, APPEND, FETCH, INBOX,
512KB) are crisply rendered as real fixed-width inscriptions. The
interior of the pot is unmarked — Gherkin lives ONLY on the outer wall,
visible from outside.

LIGHTING HIERARCHY —
- Brightest anchor: the engraved Gherkin text on the outer wall of the
  pot. It is lit from above by the wide falling stream and from within
  by the rising molten bronze level inside the pot — a warm gold
  illumination spilling over the rim. The keywords Scenario, Given,
  When, Then catch this light most intensely, glowing warm gold against
  the dark, sooty clay.
- Secondary: the wide falling stream itself.
- Tertiary: sparks rising from inside the pot where the stream impacts
  the molten pool, embers floating upward.
- Ambient: the distant forge at the right frame edge — deep warm red.
- Everything else: sooty darkness, rough textures lit only by reflection.

ATMOSPHERE — heavy drifting smoke filling the upper third of frame, fine
sparks rising from inside the pot, pronounced heat shimmer above the pot
rim distorting the smoke, fine particulate dust suspended in the lit
air, slight motion blur on the falling stream.

PALETTE — deep charcoal blacks, sooty browns, weathered stone gray,
warm orange-red mid-tones, brilliant warm gold on the lit Gherkin
engraving. Almost monochromatic in the shadows; the only saturated
colour is heat itself.

TEXTURE — visible patina and corrosion on the iron chain, deep grain on
the oak workbench, hand-thrown imperfections and clay grain on the pot
walls, viscous flowing surface on the molten bronze, gritty calloused
skin on the human hand.

MOOD — reverent, focused, ancient craft meeting precise modern
specification. A moment of transformation. The vessel is sacred; the
spec engraved on its outer wall is the visible truth, and the code-stream
pouring in becomes its substance.

NEGATIVE — Absolutely NO C source code visible anywhere outside the
falling molten stream. NO code captions, NO labels, NO floating
annotations, NO HUD elements, NO speech bubbles, NO sticky notes, NO
secondary text panels, NO subtitles. Every single C glyph in the entire
frame must live inside the dense flowing molten mass and nowhere else;
the rest of the frame contains only the engraved Gherkin on the outer
pot wall and no other readable text. NO text or engraving on the pot's
interior. NO flat slab mold, NO two-part split mold, NO tray. NO
watermarks, NO signatures, NO logos, NO UI elements, NO decorative
borders, NO overlay title.
```
