# LIM 0003: V1 does not specify unknown zones and malformed Pub/Sub envelopes

- **Status:** Accepted
- **Resolution intent:** must-resolve (technical debt)
- **Date proposed:** 2026-11-13
- **Date approved:** 2026-11-13
- **Proposed by:** EquiGuard Architecture Team
- **Approved by:** Workshop Lead
- **Scope:** `geofence-processor` input handling (`POST /telemetry-push`)
- **Related ADRs:** [ADR-0002](../adr/0002-event-driven-pubsub-push-to-cloud-run.md), [ADR-0003](../adr/0003-firestore-persistence-and-alert-schema.md)
- **Related Guidelines:** BDD Guidelines v1.9.0 §4.5 (error path enumeration), §14 (Specification Critic)

## Resolution intent

**Classification: must-resolve.**

V1 specifies the behaviour for valid telemetry and for telemetry with missing mandatory fields (HTTP `400`). Two inputs are deliberately left unspecified: a ping whose `zone` has no document in `geofences`, and a Pub/Sub push envelope that is itself malformed (invalid base64, missing `message`).

## Context

The error path enumeration ([`bdd/00_error_path_enumeration.md`](../../bdd/00_error_path_enumeration.md), rows 2.4 and 2.5) lists both cases. In V1, operators seed `geofences/<zone>` before a collar is activated, and the outer envelope is produced by the managed Pub/Sub service, not by clients.

## Nature of the weakness

- **Unknown zone:** No scenario fixes the HTTP status or states that no alert is written when `geofences/<zone>` does not exist.
- **Malformed envelope:** No scenario fixes the reaction to invalid base64 or a missing `message` object; only missing fields inside a valid envelope are specified (HTTP `400`).

## Why the clean solution is not chosen

Both cases need an operator-facing decision (silently drop, reject with `4xx`, or alert operators) that V1 does not have. Specifying a status code now would freeze a behaviour nobody has decided.

## Mitigations in place

1. Rows 2.4 and 2.5 of the error path enumeration are marked `none` with this LIM as the reason.
2. An AI agent reading this LIM knows the behaviour is open and must not present any choice as specified.

## Residual risk

A ping for a zone that was never seeded, or a corrupted envelope, may be rejected, dropped or retried by Pub/Sub depending on the implementation.

## Triggers for revisit

- Operator alerting for misconfigured collars.
- Clients other than the managed Pub/Sub push subscription.

## References

- [ADR-0002](../adr/0002-event-driven-pubsub-push-to-cloud-run.md)
- [ADR-0003](../adr/0003-firestore-persistence-and-alert-schema.md)
- [`bdd/00_error_path_enumeration.md`](../../bdd/00_error_path_enumeration.md)
