# Prompt v3 — LOTR pivot, three-quarter view, primitive cauldron

Iteration after v2 render. The geometry of v2 (centred crucible, wide
stream, vessel with external Gherkin) is retained. What changes:
perspective shifts to 3/4, the vessel becomes a primitive scorched-black
forge-cauldron, the cinematic reference layers Andrew Lesnie's LOTR over
Roger Deakins, and full readability is replaced by partial recognition.

```
Photorealistic cinematic frame, 16:9 anamorphic widescreen. Visual
language: a fusion of Roger Deakins' chiaroscuro and Andrew Lesnie's
Lord of the Rings cinematography (Mount Doom forge, the foundries of
Khazad-dûm, the casting of the rings of power). Mythic weight. Heavy
volumetric haze pierced by warm god-rays. Crushed but textured shadows.
Earthy LOTR colour grading: deep cool grey-green shadows against
saturated warm-orange highlights. Fine natural film grain.

SETTING — An ancient, soot-encrusted forge deep in a stone hall, late at
night. Almost everything beyond the central action recedes into thick
atmospheric haze and shadow. A faint distant red glow at the far right
edge hints at a deeper fire chamber. The stone walls are barely
suggested, their texture only implied by edge light. A heavy iron-bound
oak workbench, charred and weathered, supports the central vessel.

COMPOSITION (medium shot, three-quarter view) —

Camera angle: positioned approximately thirty degrees OFF the frontal
axis, slightly above eye level, looking down at a moderate angle onto
the central action. This is NOT a flat frontal composition — the
vessel turns visibly, showing the curvature of its body and the wrap
of the inscription around its surface. The far side of the cauldron
falls into shadow.

Crucible (centre-rear, upper third of frame, dominant in scale): a
massive, heavy, soot-blackened bronze crucible suspended from above by
thick iron chains. The crucible is tilted forward, pouring directly
downward. It is closer to the camera than in earlier compositions —
weighty, ancient, with deep patina and corrosion visible on its
surface, dwarven in character.

Hand on tilting chain: at the left frame edge, a single bare human
hand — large, calloused, knuckles black with carbon dust, dirt under
the fingernails, weathered skin, NO glove — grips the iron tilting
chain firmly. Only the hand and a sliver of forearm are visible.

The pour (centre vertical axis, slightly turned with perspective): a
WIDE, THICK, viscous column of molten matter falls from the crucible
mouth into the open mouth of the cauldron. Embedded THROUGHOUT the
falling mass — never beside it, never as floating overlay — are large
luminous C source code glyphs. Recognisable tokens float and tumble
inside the molten flow itself: pthread_create, cache_entry_t *entry,
queue_push(ctx, "INBOX", ...), pointer asterisks, struct braces,
semicolons. Glyphs are LARGE — white-hot yellow at the top of the
stream where they remain intact; softening to incandescent orange in
the middle as they deform; dissolving into pure molten bronze at the
bottom where the stream enters the cauldron. PARTIAL recognition is
enough — some glyphs distinct, others already smearing — the viewer
should clearly see "code is in here" without being asked to read it.

The cauldron (centre-foreground, dominant in frame): a massive, heavy,
PRIMITIVE forge cauldron — emphatically NOT a refined kitchen
ceramic. Material: dark-fired charcoal-black clay, almost obsidian in
tone, with raw soot encrustation, deep scorching, and visible cracks
from repeated firings. The surface is COARSE, IRREGULAR, hand-hewn,
with heavy thumb marks, uneven walls, patches of accumulated black
residue, and rough texture. Bound at the base and rim by dark iron
strapping with rusted rivets. Massive and squat, planted firmly on the
workbench. The mouth is wide and slightly irregular. This is a
dwarven-forge vessel from a hall under the mountain — ancient, ritual,
weighty.

On the OUTER wall of the cauldron, facing roughly toward the camera
but wrapping around the curvature, DEEPLY INCISED raised-relief
Gherkin inscriptions read fragments of:

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

The inscription is genuinely THREE-DIMENSIONAL — chiselled deep into
the black clay, casting hard shadows inside each letter, with warm
bronze highlights along the upper edges of the raised letterforms.
This is NOT painted text on a surface; it is physical relief carved
into the vessel's wall. The FRONT-FACING portion of the inscription is
clearly recognisable — keywords like Scenario, Given, When, Then catch
the warm light along their upper edges, and tokens like APPEND, INBOX,
GCS, FETCH are legible — while the WRAPPING SIDE of the inscription
falls into deep shadow and partial illegibility. Partial recognition
is the explicit intent.

LIGHTING HIERARCHY —
- Brightest: the wide pour itself and the warm glow rising from inside
  the cauldron's mouth.
- Strong secondary: the front-facing inscription on the cauldron wall,
  catching warm side-light from the stream and rising bronze level
  inside. The 3D letterforms cast hard shadows into their own incised
  depth — that shadow play IS the readability.
- Tertiary: sparks and embers rising from the cauldron's interior.
- Ambient: faint distant forge red on the right edge.
- Everything else: deep crushed shadow, only suggested by edge light.

ATMOSPHERE — heavy volumetric haze and drifting smoke filling the upper
two-thirds of frame, sharp god-rays of warm light cutting through the
smoke where they pass the stream, fine sparks rising from inside the
cauldron, pronounced heat shimmer above the rim, fine ash and
particulate dust suspended in the air, slight motion blur on the
falling stream.

PALETTE — crushed charcoal blacks, cool grey-green shadows, sooty
browns, saturated warm-orange and gold mid-tones, brilliant white-hot
yellow at the heart of the stream. LOTR-style warm-cool contrast.
Almost no saturated colour outside the heat itself.

TEXTURE — deep patina and corrosion on the iron chain and crucible;
rough scorched grain on the cauldron walls with visible cracks, soot
encrustation, and irregular thumbprints from hand-throwing; oxidised
iron strapping with rusted rivets binding the cauldron base and rim;
deep oak grain on the workbench; viscous flow on the molten bronze;
gritty calloused skin on the human hand.

MOOD — mythic, weighty, ancient. The act is sacred, ritual, dangerous.
The setting evokes a forge below the world — Mount Doom, Khazad-dûm,
the casting of the rings of power. Modern specification meets
primordial craft.

NEGATIVE — Absolutely NO C source code visible anywhere outside the
falling molten stream. NO code captions, NO labels, NO floating
annotations, NO HUD elements, NO subtitles, NO secondary text panels.
Every C glyph in the entire frame must live inside the dense flowing
molten mass and nowhere else. NO refined kitchen-pottery or
soup-tureen look on the cauldron — it must read as primitive,
scorched, hand-hewn, dwarven-forge weight. NO flat frontal
composition — the vessel and crucible are seen at a clear angle. NO
painted-on lettering — every visible Gherkin character is physically
chiselled in 3D relief, casting its own shadow. NO text or engraving
on the cauldron's interior. NO flat slab mold, NO two-part split
mold, NO tray. NO watermarks, NO signatures, NO logos, NO UI
elements, NO decorative borders, NO overlay title.
```
