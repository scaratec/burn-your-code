# ADR 0001: Point-in-polygon geofence evaluation via ray casting

- **Status:** Accepted
- **Date:** 2026-11-10
- **Deciders:** EquiGuard Architecture Team

## Context

EquiGuard receives GPS telemetry pings (`lon`, `lat`, `timestamp`, `device`, `zone`) from collars on grazing horses. For every ping, the system must determine whether the coordinate `(lon, lat)` lies inside or outside the closed pasture polygon configured for `zone`.

The pasture polygon is operator-defined: an ordered list of `{lon, lat}` vertices (between 3 and ~100 vertices, where the last vertex closes back to the first). Polygons may be convex (`HomePasture`, 5 vertices) or complex concave shapes with interior cutouts (`ComplexPasture`, 23 vertices).

## Decision

We use the **even-odd ray-casting algorithm** (Jordan curve theorem) implemented directly in the service's domain layer without external GIS or geometry libraries:

- Cast a horizontal ray from the test point `(lon, lat)` and count intersections with the polygon's edges.
- If the intersection count is odd, the point is **inside** (`true`); if even, the point is **outside** (`false`).
- Coordinates are IEEE-754 double-precision floats (`lon` = longitude, `lat` = latitude).

## Consequences

### Positive

- Zero external geometry dependencies in any target language (Go, Python, Rust, TypeScript, Java).
- Handles both simple convex polygons (`HomePasture`) and complex concave polygons (`ComplexPasture`) in ~25 lines of pure code.
- Deterministic and fast ($O(n)$ in vertex count $n$), testable in complete isolation via Milestone 1 (`@mi1`).

### Negative

- Hand-rolled geometry logic must be verified against both convex and concave polygons in the BDD suite.
- V1 evaluates each ping against a single polygon array per pasture (see [LIM-0001](../limitations/0001-single-static-polygon-per-pasture.md)).

### Neutral

- Planar ray casting is accurate for pasture-scale polygons (hundreds of meters) in mid-latitudes without geodesic projection.

## Security Implications

The algorithm is a pure function over in-memory numbers: it performs no I/O, crosses no trust boundary, and logs no data. Polygon vertices come from trusted operator master data in Firestore (`geofences` collection); incoming telemetry coordinates are parsed as numbers and validated before evaluation ([ADR-0002](0002-event-driven-pubsub-push-to-cloud-run.md)).

## Alternatives Considered

- **Winding number algorithm.** Rejected because its trigonometric/angle summation adds complexity without changing the result for non-self-intersecting pasture polygons.
- **External GIS library (e.g., GEOS, Shapely, Turf.js, `paulmach/orb`).** Rejected because it couples the specification to language-specific libraries and native C bindings for a 25-line algorithm.
- **Database spatial query (PostGIS / BigQuery GIS).** Rejected because Firestore is our operational store ([ADR-0003](0003-firestore-persistence-and-alert-schema.md)) and in-process evaluation avoids an extra network hop per ping.

## References

- Enforced by: [`bdd/mi1_geofence_library.feature`](../../bdd/mi1_geofence_library.feature) (`HomePasture` and `ComplexPasture` Scenario Outlines)
- Bounded by: [LIM-0001](../limitations/0001-single-static-polygon-per-pasture.md)
