# LIM 0001: V1 supports a single static polygon per pasture without interior exclusion zones

- **Status:** Accepted
- **Resolution intent:** must-resolve (technical debt)
- **Date proposed:** 2026-11-10
- **Date approved:** 2026-11-10
- **Proposed by:** EquiGuard Architecture Team
- **Approved by:** Workshop Lead
- **Scope:** `geofence-processor` Firestore schema and point-in-polygon evaluation
- **Related ADRs:** [ADR-0001](../adr/0001-point-in-polygon-ray-casting.md), [ADR-0003](../adr/0003-firestore-persistence-and-alert-schema.md)
- **Related Guidelines:** BDD Guidelines v1.9.0 §2.3 (variance), §14 (Specification Critic)

## Resolution intent

**Classification: must-resolve.**

V1 of EquiGuard stores a single `polygon` vertex array per document in `geofences/<zone>`. Multi-polygon pastures and polygons with interior exclusion rings ("holes", such as a fenced-off pond inside a pasture) are deferred to V2.

## Context

In [`bdd/mi1_geofence_library.feature`](../../bdd/mi1_geofence_library.feature), the second Scenario Outline is titled *"Validate complex concave geofence with interior exclusions"* (`ComplexPasture`), where an interior indentation is modeled as a single continuous self-wrapping concave boundary (a C-shaped corridor) rather than a GeoJSON multi-ring polygon with separate outer and inner rings. Similarly, Firestore documents in `geofences/<zone>` contain a single flat `"polygon": [{"lon": ..., "lat": ...}, ...]` array ([ADR-0003](../adr/0003-firestore-persistence-and-alert-schema.md)).

## Nature of the weakness

- **1:1 Zone-to-Polygon mapping:** A pasture consisting of two disconnected paddocks cannot be represented as one zone.
- **No separate inner-ring array:** Excluded areas inside a pasture must either be connected to the outer boundary via a narrow concave channel (as in `ComplexPasture`) or omitted via a conservative boundary.

## Why the clean solution is not chosen

Keeping the schema to `{"polygon": [{"lon": ..., "lat": ...}]}` keeps the workshop's data model and ray-casting loop compact enough to be specified, audited, and autonomously implemented within a single workshop session.

## Mitigations in place

1. `ComplexPasture` in [`bdd/mi1_geofence_library.feature`](../../bdd/mi1_geofence_library.feature) tests a 23-vertex concave polygon to ensure the ray-casting implementation handles non-convex geometry accurately.
2. The single-array schema is explicitly specified in `Background` docstrings across `mi2`, `mi3`, and `mi4`.

## Residual risk

Operators with truly disjoint sub-pastures must configure separate zones (`HomePastureA`, `HomePastureB`) in V1.

## Triggers for revisit

- Onboarding a farm that requires GeoJSON `Polygon` (outer ring + holes) or `MultiPolygon` support.

## References

- [ADR-0001](../adr/0001-point-in-polygon-ray-casting.md)
- [ADR-0003](../adr/0003-firestore-persistence-and-alert-schema.md)
- [`bdd/mi1_geofence_library.feature`](../../bdd/mi1_geofence_library.feature)
