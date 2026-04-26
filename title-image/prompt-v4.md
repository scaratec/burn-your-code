# Prompt v4 — iron cauldron, intaglio inscription, stream-as-relief code

Iteration after v3. Same LOTR atmosphere, same composition, same
scenario text. Three structural fixes target the model's persistent
defaults: cauldron switches from clay to forged iron (solves
not-black-enough by material rather than colour bribe); code is
re-framed as 3D relief sculpted FROM the stream's own substance (solves
side-caption by making code geometrically inseparable from flow);
engraving switches from raised relief to sunken intaglio (solves
painted-glow-text because intaglio HAS no glow — it is shadow-shape).

```
CRITICAL CONSTRAINTS — read first, apply throughout:

(1) Every C source code form visible anywhere in the entire frame is
    sculpted in 3D RELIEF from the molten stream's own surface. The
    code is the same material as the stream, the same temperature, the
    same glow. Code shapes are extrusions of the stream's substance,
    distinguished from smooth flow only by the ridge-light catching
    their raised edges and the recess-shadow between them. There is NO
    floating code caption, NO code label, NO painted code text, NO HUD
    overlay anywhere in the frame. Code lives only as relief in the
    flow.

(2) Every Gherkin inscription on the cauldron is INTAGLIO — sunken,
    chiseled INTO the iron surface, recessed below the surrounding
    metal. The letterforms are NEGATIVE SPACE: dark hollows that catch
    shadow. They DO NOT GLOW. They have no internal light source. They
    are visible only because warm rim-light from the stream rakes
    across the iron surface and falls into their carved channels,
    casting shadow against the iron's edge. NOT painted. NOT raised
    above the surface. NOT self-luminous.

Photorealistic cinematic frame, 16:9 anamorphic widescreen. Visual
language: Andrew Lesnie's Lord of the Rings cinematography fused with
Roger Deakins chiaroscuro — Mount Doom's forge, the Cracks of Doom,
the hidden foundries of Khazad-dûm. Mythic ritual weight. Heavy
volumetric haze pierced by warm god-rays from above. Crushed cool
grey-green shadows against saturated warm-orange highlights. Fine
natural film grain.

SETTING — A vast forge hall hewn from black stone, late at night.
Massive arched stone pillars recede into thick atmospheric haze. A
faint deep-red glow at the right edge hints at the main fire chamber.
The action sits on a heavy iron-bound oak workbench, charred and
weathered.

COMPOSITION (medium shot, three-quarter view, ~30° off frontal axis,
slightly above eye level) —

Crucible: massive, soot-blackened bronze, torso-sized, suspended from
above by thick iron chains, dominating the upper-centre of frame. The
crucible is tilted forward, pouring directly downward. Heavy, ancient,
deeply patinaed.

Hand on tilting chain: at left frame edge, a single bare human hand —
large, calloused, knuckles black with carbon dust, dirt under
fingernails, weathered like sandstone with every line and crack
visible, NO glove. Only hand and a sliver of forearm visible.

The pour (centre vertical axis): a wide, thick, viscous cylinder of
molten matter falls from crucible into cauldron. The stream's surface
is sculpted: on its front-facing face, recognisable C source code
forms RISE FROM THE FLOW AS 3D RELIEF — pthread_create,
cache_entry_t *entry, queue_push(ctx, "INBOX", ...), pointer asterisks,
struct braces, semicolons. Each letter and symbol is an extrusion of
the molten material itself; same colour, same heat, same substance —
only the angle of the surface and the cast of micro-shadows in the
relief makes them readable. White-hot yellow at the top of the stream
where the relief is sharp; softening to incandescent orange in the
middle as the surface relief blurs and runs; pure smooth molten bronze
at the bottom where the stream enters the cauldron and the code has
fully dissolved. Partial recognition is enough — some code shapes
distinct, others already smearing back into pure flow.

The cauldron (centre-foreground, dominant in frame): a massive
hand-forged BLACK IRON cauldron — wrought iron, NOT clay, NOT ceramic,
NOT pottery. The body is built from heavy iron plates joined with
deep-driven rivets, finished with hammer-marked surface texture,
oxidised black patina, soot encrustation, and scorched darkening
around the rim from countless previous pours. Reinforced by thick iron
bands at the base and rim. Iron carrying rings hang from the sides.
The mouth is wide, slightly irregular. Squat, massive, planted firmly
on the workbench. This is a dwarven-forge vessel — a relic from a
hall under the mountain.

On the OUTER iron wall of the cauldron, facing roughly toward the
camera and wrapping around the curvature, the Gherkin inscription is
CHISELED INTO the iron AS INTAGLIO — sunken cuts forming letterforms.
The carved channels are darker than the surrounding iron because they
hold deeper shadow. The inscription, fragments of which are visible:

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

The front-facing portion of the inscription is recognisable through
the shadow-relief — keywords like Scenario, Given, When, Then read via
the deep shadow inside their carved channels, with warm light catching
only the upper edge of each cut. The wrapped/far side of the
inscription falls fully into shadow and becomes illegible. Partial
recognition is the intent.

LIGHTING HIERARCHY —
- Brightest: the molten pour and the warm glow rising from inside the
  cauldron's mouth.
- Strong secondary: the front face of the iron cauldron, catching sharp
  warm side-light from the stream — the side-light rakes across the
  iron surface and falls into the chiseled letter-channels, revealing
  the inscription via cast shadow against iron.
- Tertiary: sparks and embers rising from inside the cauldron.
- Above: warm volumetric god-rays piercing the haze from off-frame.
- Ambient: faint deep-red from the distant fire chamber on the right
  edge.
- Everything else: deep crushed shadow.

ATMOSPHERE — heavy volumetric haze and drifting smoke filling the upper
half of frame, sharp god-rays of warm light raking down through the
smoke from above, fine sparks rising from the cauldron, pronounced
heat shimmer above the rim, fine ash and dust suspended in the lit
air, slight motion blur on the falling stream.

PALETTE — crushed charcoal blacks, cool grey-green shadows, sooty
browns, saturated warm-orange and gold at heat sources, brilliant
white-hot yellow at the heart of the stream. Iron reads as deep black
with thin warm edge-light only. No painted-glow accents.

TEXTURE — deep oxidation, pitting and hammer marks on all iron
surfaces (chain, crucible, cauldron); rivet seams and iron-band
junctions on the cauldron walls; carved shadow-channels of the
intaglio inscription cut deep into the iron; viscous flowing surface
of the molten bronze with raised code-relief on the front face;
gritty sandstone-like skin on the human hand with deep weathered
creases.

MOOD — mythic, weighty, ritual. The casting of code into spec is
performed as sacred ancient craft. Mount Doom undertones.

NEGATIVE — no painted lettering anywhere in the frame; no glowing
floating captions or labels; no HUD or annotation text; no clay,
ceramic, or pottery material on the cauldron; no frontal/flat
composition; no raised-relief inscription on the cauldron (intaglio
only); no self-luminous letters; no watermarks, no signatures, no
logos, no UI, no decorative borders, no overlay title.
```
