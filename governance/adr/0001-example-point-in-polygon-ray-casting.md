# ADR 0001: Point-in-polygon — ray casting over winding number

> **Worked example.** This ADR is illustrative; it documents a
> decision in the [EquiGuard workshop](../../workshop/) domain
> (a GPS-based geofencing system that decides whether a horse
> has left a pasture polygon). Adapt the form to your own
> project; the discipline is in the structure, not the content.

- **Status:** Accepted
- **Date:** 2026-04-15
- **Deciders:** EquiGuard team

## Context

EquiGuard receives GPS telemetry pings (latitude, longitude,
timestamp) from collars on grazing horses. For every ping, the
geofence-processor must decide *is this point inside the
configured pasture polygon?* and emit an alert if a previously
inside-the-polygon horse has just transitioned to outside.

The polygon is operator-defined: an arbitrary closed shape with
between 3 and roughly 100 vertices. It can be convex or concave,
but it is always simple (no self-intersections — operators draw
it once in the configuration UI; the UI rejects self-crossing
shapes at edit time).

Two well-known algorithms are candidates:

- **Ray casting** (Jordan curve theorem): cast a ray from the
  test point to infinity; count crossings with polygon edges;
  inside iff the count is odd. O(n) per test, n = vertex count.
- **Winding number**: sum the signed angles subtended by polygon
  edges from the test point; inside iff the sum is non-zero.
  Also O(n), with a numerical-stability advantage on points
  *very close* to a vertex.

Performance is not the bottleneck — the workload is one test
per ping, and pings arrive at sub-Hz rates per horse. Code
simplicity, testability, and the presence of well-trodden
implementations matter more than the constant factor.

## Decision

We use the **ray casting** algorithm, implementing it from
first principles in `internal/geofence/contains.go` rather than
importing a geometry library.

The choice is motivated by three properties:

- The algorithm fits in ~30 lines of Go and is fully covered by
  the BDD scenarios in `bdd/features/point_in_polygon.feature`.
- The "point exactly on an edge" edge-case is decidable by a
  documented convention (we treat boundary points as inside),
  rather than by relying on a library's silent default.
- It avoids a transitive dependency on a geometry crate for a
  60-line piece of business logic.

## Consequences

### Positive

- The implementation is short, auditable, and fully covered by
  Gherkin scenarios. A new contributor can read the algorithm
  in five minutes.
- Edge-case behaviour (point on a vertex, point on an edge,
  ray that grazes a vertex) is decided by us, not by the
  library, and is asserted explicitly in the BDD suite.
- No dependency on a geometry library that might bring its own
  numerical-stability assumptions or licensing constraints.

### Negative

- We hand-implement a textbook algorithm. A bug in the
  implementation would be ours to find, not a library
  maintainer's.
- The numerical-stability edge cases that winding number
  handles cleanly (points within ε of a vertex on a long edge)
  are still potential traps for us, even if BDD covers the
  most common shapes.

### Neutral

- The choice is reversible: the public function signature
  `Contains(polygon []Point, p Point) bool` is algorithm-
  agnostic. Swapping in winding number later is a one-file
  change.

## Security Implications

The algorithm runs against operator-supplied polygon vertices
and GPS-supplied test points. Both are size-bounded by
upstream validation (polygon ≤ 100 vertices at upload time;
GPS coordinates fit in a fixed-size struct). A malicious
operator who could submit a 10-million-vertex polygon would
DoS the geofence-processor — but this is bounded by the
upload-side validation, not by the algorithm.

The algorithm reads no external state, writes no external
state, and emits no logs. It is pure. There are no trust
boundaries crossed inside the function. The Pub/Sub-attribute
write that *acts* on the result is a separate decision (see
the workshop's main pipeline).

## Alternatives Considered

- **Winding number algorithm.** Rejected because the
  numerical-stability advantage is not material for our input
  shapes (operator-drawn pastures, never spiky), and the BDD
  edge-case scenarios are clearer to author against ray
  casting's "count crossings" mental model than against
  winding number's "sum angles" one.
- **Import `github.com/paulmach/orb` or similar geometry
  library.** Rejected on the basis of "60-line problem ⇒ no
  external dependency". The library's own edge-case
  conventions (boundary inclusion, degenerate polygons) would
  also have needed to be asserted by our BDD suite, leaving
  us with the same scenarios *plus* the dependency.
- **PostGIS / Cloud Spanner spatial query.** Rejected as
  architecturally out of scope. The geofence-processor is a
  Cloud Run service that decides per-ping in-process; pushing
  the test into a database query would add an RPC per ping
  for no observable benefit.

## References

- [Jordan curve theorem (Wikipedia)](https://en.wikipedia.org/wiki/Jordan_curve_theorem)
- [Point in polygon — ray casting (Wikipedia)](https://en.wikipedia.org/wiki/Point_in_polygon#Ray_casting_algorithm)
- `bdd/features/point_in_polygon.feature` — the contract this
  ADR satisfies.
- No related Limitation Records at this time.
