# Prompt v6 — wide viscous flow, 90°-rotated code, side-view inscription

Iteration after v5. Found-photograph aesthetic and weathered inscription
are kept. Four structural changes: the stream is rotated 90° relative
to the code (text runs ALONG the flow direction); stream becomes much
wider and more viscous; cauldron is rotated to show inscription only in
side-profile raking view; code is fully reframed as relief sculpted by
the flow's own surface. v5 is preserved unchanged.

```
CRITICAL CONSTRAINTS — read first, apply throughout:

(1) This image must read as a FOUND DOCUMENTARY PHOTOGRAPH, not a
    constructed CGI concept render. Embrace asymmetry, selective
    focus, foreground occlusion, hand-held framing, film-stock
    imperfection. Compositional perfection is forbidden.

(2) The pour is a MASSIVE, ROPEY, HEAVILY VISCOUS column of molten
    matter — at least the thickness of a strong man's forearm,
    slow-falling under its own weight, with visible surface tension
    and a slight rope-like pulse in its diameter. It moves like
    molten gold or thickest honey, NOT like thin-flowing water. It
    dominates the frame as a substantial physical mass.

(3) C source code is sculpted INTO this wide stream's front surface
    as deep 3D RELIEF — large letterforms occupying significant area
    on the stream's face. The letters are ROTATED 90° relative to
    the camera so that the lines of code run ALONG the direction of
    the fall: each letter's long axis runs PARALLEL TO GRAVITY, as
    if the code were engraved DOWN the length of a falling pillar.
    A normal reader would have to tilt their head 90° to read them.
    The letters are made of the SAME molten material as the stream
    itself — same colour, same heat, same substance — distinguished
    from the smooth flow only by ridge-light catching their raised
    edges and recess-shadow between them. The code IS the surface
    of the stream. There is NO floating caption, NO overlay, NO
    label, NO text hovering beside or over the flow.

(4) The Gherkin inscription on the cauldron is visible ONLY FROM A
    STEEP SIDE-RAKING ANGLE — the cauldron is rotated so its
    inscription face points away from the camera, and we see the
    inscription only as it wraps around the iron body's curving
    side, catching warm raking light along chiseled cuts. NO
    portion of the inscription faces the viewer head-on. Most of
    it is implied through partial words and isolated letterforms
    grazing past as the iron curves out of sight. NEVER fully
    legible from this angle.

Photorealistic frame, 16:9 anamorphic widescreen. Visual language:
Andrew Lesnie's LORD OF THE RINGS atmosphere (Mount Doom forge,
Khazad-dûm halls, mythic ritual weight), Roger Deakins chiaroscuro
lighting, Sebastião Salgado documentary foundry photography (Workers
series — found moment, witness perspective). Captured on Kodak
Vision3 800T tungsten film: visible grain, mild halation around
brightest highlights, soft natural depth-of-field falloff, hand-held
slightly off-axis framing, selective focus.

SETTING — A vast forge hall hewn from black stone, late at night.
Massive arched stone pillars recede into thick atmospheric haze. A
faint deep-red glow at the right edge hints at the main fire chamber.
Heavy iron-bound oak workbench, charred and weathered.

COMPOSITION (medium shot, strong side-angle ~60° off the cauldron's
inscription axis, slightly above eye level — asymmetric, off-centre,
witness-perspective) —

The camera sits to the LEFT of the cauldron's inscription face. The
cauldron is rotated so its inscribed wall faces obliquely AWAY from
the lens; we see the iron body in three-quarter profile, with the
inscription wrapping around the far-right curve of the body and
visible only as raking-light shadow play at that curve.

Crucible: massive, soot-blackened bronze, torso-sized, suspended
from above by thick iron chains, dominating the upper-centre of
frame. Tilted forward, pouring downward. Heavy, ancient, deeply
patinaed; iron banding at the base.

Hand on tilting chain: at left frame edge, a single bare human hand
— large, calloused, knuckles black with carbon dust, dirt under
fingernails, weathered like sandstone, NO glove. Slightly out of
sharp focus — the lens has chosen the stream and cauldron, not the
hand.

THE POUR — primary subject of the frame:

A WIDE, VISCOUS, ROPEY column of molten matter falls from the
crucible mouth into the cauldron. Its thickness is substantial — at
least a strong forearm in diameter, with slight irregular pulse
along its length where the viscosity bunches and stretches. The
flow is slow and heavy, like molten gold dripping under its own
weight. Surface tension visible at the boundary; faint molten skin
forming and breaking. Sparks pop where the falling matter hits the
rising bronze pool inside the cauldron.

ON THE FRONT-FACING SURFACE OF THIS WIDE POURING COLUMN, sculpted
in deep 3D RELIEF FROM THE MOLTEN MATERIAL ITSELF, large C source
code forms run DOWN THE LENGTH OF THE FLOW with each letter
ROTATED 90° from the camera's upright orientation. Lines of code
read top-to-bottom along the falling direction. Recognisable
fragments emerge clearly — pthread_create, cache_entry_t *entry,
queue_push(ctx, "INBOX", ...), pointer asterisks, struct braces,
semicolons — all rendered as relief in the same glowing material
as the stream itself. The letters are large enough to read if the
viewer tilts their head 90°. White-hot at the top of the stream
where the relief is sharp; softening to incandescent orange in the
middle as the surface relief blurs and runs; pure smooth molten
bronze at the bottom where the stream enters the cauldron and the
code has fully dissolved into uninterrupted flow. Partial
recognition is enough. The code IS the surface of the matter, NOT
overlaid text.

The cauldron (centre-foreground left of true centre, dominant in
silhouette but secondary to the stream): a massive hand-forged
BLACK IRON cauldron — wrought iron plates joined by deep-driven
rivets, hammer-marked surface, oxidised black patina, soot
encrustation, scorched darkening, iron banding at base and rim,
iron carrying rings on the sides. Body shows real history: a faint
dent above one of the carrying rings, one plate visibly larger from
re-welding, a hairline crack stopped by a thick rivet patch,
asymmetric belly bulge from heat-cycling. Squat, massive, planted
on the workbench.

Because of the side angle, only the LEFT EDGE of the cauldron's
inscribed face is visible, curving away from the camera. There an
ancient weathered inscription is chiseled into the iron — Roman-
capital letterforms cut centuries ago by a stonemason's hand, now
deeply soot-clogged, oxidised, and partially obliterated by
hairline cracks and patina. From this side angle we catch only
fragments grazing past as the iron's curve takes them out of
view: perhaps a single word like 'Scenario' or 'APPEND', a fragment
like '@security' or '512KB' or 'INBOX', a partial line like
'must complete' — each lit by raking warm light catching the upper
edges of chiseled cuts and casting long shadows into their depths.
The full inscription, partially recoverable from these fragments,
is the BDD scenario:

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

But in the rendered image, the inscription is mostly hidden by the
side angle and the curvature of the iron body — only fragments
catch the light. The inscription is NOT painted, NOT self-luminous,
NOT facing the camera, NOT cleanly readable.

A wisp of dense smoke curls across the LOWER LEFT FOREGROUND,
slightly out of focus, partially occluding the bench edge — the
camera shoots THROUGH the environment.

LIGHTING HIERARCHY —
- Brightest: the wide molten pour itself — the central subject.
  Mild halation around the highlights from the film stock.
- Strong secondary: warm light spilling from the cauldron's mouth
  onto the rim and curving body, raking across whatever inscription
  fragments curve into view.
- Tertiary: scattered sparks and embers rising from the cauldron.
- Above: warm volumetric god-rays piercing the haze.
- Ambient: faint deep-red from the distant fire chamber on the right.
- Everything else: deep crushed shadow.

ATMOSPHERE — heavy volumetric haze and drifting smoke filling the
upper half of frame, sharp god-rays raking through, fine sparks
rising from the cauldron, pronounced heat shimmer above the rim,
fine ash and dust suspended in the lit air, the foreground smoke
wisp curling across lower left, slight motion blur on the falling
stream.

PALETTE — crushed charcoal blacks, cool grey-green shadows, sooty
browns, saturated warm-orange and gold at heat sources, brilliant
white-hot yellow at the heart of the stream. Iron near-black with
thin warm edge-light. Slight desaturation in mid-tones from film
stock. No painted-glow accents.

TEXTURE — deep oxidation, pitting, hammer marks on iron; rivet seams,
weld beads, repair patches, hairline cracks on the cauldron;
soot-clogged channels of the eroded inscription; viscous flowing
surface of the molten bronze with deep code-relief running along
the flow's length; gritty sandstone-like skin on the human hand;
visible film grain across the entire image; mild halation around
the brightest highlights.

MOOD — mythic, weighty, ritual, captured as found documentary
moment. Mount Doom undertones, Salgado eye, Lesnie palette.

NEGATIVE — no painted lettering anywhere; no glowing floating
captions or labels; no HUD or annotation text; no clay, ceramic,
or pottery on the cauldron; no inscription facing the camera
head-on; no upright-oriented code text in the stream (all stream
code is rotated 90° to the camera); no thin-water flow (the pour
is heavy, viscous, ropey); no flat frontal composition; no
perfectly centred elements; no tripod-locked architectural
framing; no raised-relief inscription on the cauldron (intaglio,
weathered, partial, side-only); no self-luminous letters; no
tack-sharp full-frame focus; no clean fully-readable inscription;
no watermarks, no signatures, no logos, no UI, no decorative
borders, no overlay title.
```
