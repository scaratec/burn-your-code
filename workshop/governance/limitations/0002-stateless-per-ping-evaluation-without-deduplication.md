# LIM 0002: V1 evaluates each ping statelessly without state-transition tracking or deduplication

- **Status:** Accepted
- **Resolution intent:** must-resolve (technical debt)
- **Date proposed:** 2026-11-10
- **Date approved:** 2026-11-10
- **Proposed by:** EquiGuard Architecture Team
- **Approved by:** Workshop Lead
- **Scope:** `geofence-processor` alert emission logic (`POST /telemetry-push`)
- **Related ADRs:** [ADR-0002](../adr/0002-event-driven-pubsub-push-to-cloud-run.md), [ADR-0003](../adr/0003-firestore-persistence-and-alert-schema.md)
- **Related Guidelines:** BDD Guidelines v1.9.0 §4.5 (Error Path Enumeration), §14 (Specification Critic)

## Resolution intent

**Classification: must-resolve.**

In V1, `geofence-processor` is purely stateless with respect to horse location history: every valid telemetry ping whose coordinate lies outside the configured polygon writes a `GEOFENCE_VIOLATION` record to Firestore's `alerts` collection, regardless of whether the horse was previously inside or whether an alert was already emitted for the preceding ping.

## Context

In a production livestock monitoring system, operators typically want an alert on the *transition* from inside to outside, or rate-limited alerts while the horse remains outside, plus idempotency against Pub/Sub at-least-once redelivery (`messageId` deduplication). However, tracking per-device state transitions requires a per-horse state document and transactional compare-and-set semantics in Firestore.

## Nature of the weakness

- **No prior-state check:** A single outside ping for `"Lilly"` immediately writes a `GEOFENCE_VIOLATION` alert without requiring a preceding inside ping.
- **No deduplication across consecutive outside pings or Pub/Sub redeliveries:** Multiple outside pings for the same horse produce multiple documents in `alerts`.

## Why the clean solution is not chosen

Stateless per-ping evaluation keeps `mi2`, `mi3`, and `mi4` scenarios self-contained (one `When` event → one `Then` observation in `alerts`) without requiring multi-step state-machine setup in every scenario.

## Mitigations in place

1. The BDD scenarios in `mi2`, `mi3`, and `mi4` explicitly specify and test this exact stateless contract: one outside ping for `"Lilly"` produces a `GEOFENCE_VIOLATION` record; one inside ping for `"Honey"` produces no record in `alerts`.
2. An AI agent reading this LIM knows **not** to invent state-transition filtering that would break the single-ping scenarios in `mi2`–`mi4`.

## Residual risk

In live operation (`@mi4`), a horse remaining outside the fence or a retried Pub/Sub delivery generates repeated alert documents in Firestore.

## Triggers for revisit

- Adding a notification sink (SMS / push notification) where repeated alerts would cause alert fatigue.

## References

- [ADR-0002](../adr/0002-event-driven-pubsub-push-to-cloud-run.md)
- [ADR-0003](../adr/0003-firestore-persistence-and-alert-schema.md)
- [`bdd/mi2_geofence_processor.feature`](../../bdd/mi2_geofence_processor.feature)
