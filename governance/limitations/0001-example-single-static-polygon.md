# LIM 0001: V1 supports a single static polygon per pasture

> **Worked example.** This LIM is illustrative; it documents a
> bounded weakness in the [EquiGuard workshop](../../workshop/)
> domain (a GPS-based geofencing system that decides whether a
> horse has left a pasture polygon). Adapt the form to your
> own project; the discipline is in the structure, not the
> content.

- **Status:** Accepted
- **Resolution intent:** must-resolve (technical debt)
- **Date proposed:** 2026-04-18
- **Date approved:** 2026-04-20
- **Proposed by:** EquiGuard team
- **Approved by:** EquiGuard team lead
- **Scope:** `geofence-processor` Cloud Run service.
- **Related ADRs:** [ADR-0001](0001-example-point-in-polygon-ray-casting.md)
- **Related Guidelines:** BDD Guidelines §2.3 (variance
  scenarios), §4.3 (independent-channel verification).

## Resolution intent

**Classification: must-resolve.**

V1 of EquiGuard binds each pasture to exactly one polygon
shape, configured once and edited only via the operator UI.
Multi-polygon pastures (a pasture with a fenced-off corner;
two disjoint grazing areas with the same alert recipient;
seasonal sub-zones) are deferred. The clean V2 solution is a
small data-model change (`Pasture.polygons []Polygon` instead
of `Pasture.polygon Polygon`) plus an alert-aggregation rule
(a horse "in the pasture" iff in *any* of its polygons). Both
are scoped, just not built yet.

## Context

The current EquiGuard data model in
`internal/pasture/model.go`:

```go
type Pasture struct {
    ID        string
    Polygon   []Point   // single shape, ≥ 3 vertices
    Alerts    AlertCfg
}
```

The geofence-processor reads this struct from Firestore on
startup, caches it, and tests every incoming GPS ping against
the single `Polygon` via the ray-casting algorithm of
[ADR-0001](0001-example-point-in-polygon-ray-casting.md).

Real pastures are not always single shapes:

- A working pasture may have a fenced-off corner around a
  water tank, an electrical mast, or a known mud hole. The
  horse should *not* trigger an alert when it grazes near the
  exclusion; it *should* trigger when it leaves the outer
  fence.
- A farm may rotate animals between two physical pastures
  with the same alert recipient ("Lilly grazes pasture A
  Mon-Wed, pasture B Thu-Sun"). Today this is two `Pasture`
  records with two alert configurations; the operator
  duplicates effort.
- Seasonal grazing plans (winter sub-zone, summer sub-zone,
  same alert) face the same duplication.

V1 ignores all three cases. The operator's only workaround is
to define a single polygon that conservatively encloses
everything, which trades off alert sensitivity (false
negatives at the boundaries of the conservative shape).

## Nature of the weakness

Specifically:

- **The data model has a 1:1 Pasture-to-Polygon mapping.** A
  multi-polygon pasture cannot be represented; the operator
  must split it into N pastures, duplicating the alert
  configuration N times.
- **Alert configurations are duplicated**, not shared. An
  operator who edits one of the N alerts must remember to
  edit the others. The BDD suite has no scenario that asserts
  "all N stay in sync"; nothing prevents drift.
- **Inclusion-of-exclusion ("polygon with a hole") is not
  expressible at all.** The single-polygon algorithm cannot
  represent "inside the outer fence AND outside the
  exclusion". An operator who needs this today defines a
  conservative single polygon that omits the exclusion area
  entirely, accepting alerts that fire when the horse grazes
  legitimately near the (unmodelled) hole.
- **Telemetry burst behaviour at boundaries** is identical
  across all polygons of an N-shape pasture today (because
  there is no concept of "the polygon the horse just
  crossed"). V2 will need to decide whether transitions
  *between* sub-polygons within the same pasture trigger
  alerts (intent: no) or not.

## Why the clean solution is not chosen

V1's scope was "smallest deployable geofencing system that
handles the common case (one pasture, one shape, one alert
recipient)". The single-polygon model is faithful to that
scope. Lifting the limit before V1 ships would:

- Expand the data model (Firestore schema change, migration
  script, BDD scenarios for multi-polygon pastures, alert-
  deduplication scenarios).
- Force the operator UI to grow a "draw additional polygon"
  affordance, with the attendant UX questions (is this an
  inclusion or an exclusion? what's the visual difference?).
- Invite a multi-polygon spec-audit pass (independent-channel
  verification per BDD Guidelines §4.3 becomes more involved
  when "the message is in the right pasture" requires cross-
  checking against N polygons).

The estimated cost of the clean fix is ~3 person-weeks
(model + UI + scenarios + audit). The estimated benefit for
V1's two pilot farms (both single-pasture-single-shape) is
zero. Deferring to V2 is the right call.

## Mitigations in place

1. **The conservative-enclosing-polygon workaround is
   documented** in the operator manual at
   `docs/operator/multi-zone-pastures.md`, with the explicit
   warning that it trades alert sensitivity for V1
   simplicity.
2. **The BDD scenarios assert single-polygon behaviour
   exactly** (`bdd/features/point_in_polygon.feature`,
   `bdd/features/alert_emission.feature`). Anyone who
   accidentally introduces multi-polygon code will fail the
   single-polygon assertions, surfacing the change for
   review.
3. **The data-model field is named `Polygon` (singular).** A
   contributor who would write `pasture.Polygons[0]` finds
   no such field; they have to read the data model and
   notice the singular form, which prompts the question
   "why?".
4. **Pilot farms are single-pasture-single-shape.** No
   in-production EquiGuard deployment hits the limit during
   V1. The deferral is empirically safe for the immediate
   user base.

## Residual risk

Concretely:

> A new pilot farm is onboarded mid-V1 that has a working
> pasture with a fenced-off well in the middle. The
> operator, following the documented workaround, defines a
> conservative polygon that omits the well area. Lilly
> grazes near the well; the GPS ping lands inside the
> conservative polygon (correct), then drifts to a position
> just outside the conservative polygon but well within the
> real fence (because the conservative polygon shrunk to
> avoid the well). EquiGuard fires a "horse left the
> pasture" alert. The on-call operator drives 40 minutes to
> the farm, finds Lilly grazing peacefully near the well,
> and loses trust in the alerting system.

A second concrete scenario:

> A farm operator with two seasonal pastures (summer-zone,
> winter-zone) configures them as two separate Pasture
> records with identical alert configurations. Three months
> in, they update the alert phone number on the summer-zone
> record but forget the winter-zone one. The horse leaves
> winter-zone in March; the alert goes to a phone number
> that was disconnected last summer. The operator only
> notices when the horse is found by a neighbour the next
> morning.

Probability: low for the V1 pilot user base; moderate as
EquiGuard onboards farms with operationally common shapes.
Consequence class: false-positive alerts (loss of operator
trust) and false-negative alerts (loss of animal-welfare
assurance).

## Triggers for revisit

- **A pilot farm requests a multi-polygon pasture.** Direct
  paydown trigger; the V2 work begins.
- **An alert-divergence incident occurs** (operator edits
  one of N duplicated configurations, the others go stale).
  Hardens the case.
- **Three or more single-pasture deployments turn out to
  use the conservative-enclosing-polygon workaround**, even
  though their real shapes are multi-polygon. Indicates V1's
  workaround is functionally accepted as the product, which
  is the wrong signal.
- **A regulatory change requires precise pasture boundaries**
  (e.g. organic-farming certification with specific
  exclusion-zone rules around water sources). Forces the
  inclusion-of-exclusion data shape.

"Eventually we should support multiple polygons" is not a
trigger.

## References

- [ADR-0001 — Point-in-polygon: ray casting over winding
  number](0001-example-point-in-polygon-ray-casting.md) —
  the algorithmic decision this LIM bounds in terms of
  data-model expressivity.
- `bdd/features/point_in_polygon.feature` — the
  single-polygon contract.
- `bdd/features/alert_emission.feature` — the alert-emission
  contract whose duplication this LIM admits.
- `docs/operator/multi-zone-pastures.md` — the operator
  workaround documentation.
