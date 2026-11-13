# LIM 0003: V1 leaves unknown zones unspecified and malformed Pub/Sub envelopes untested

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

Two inputs to `POST /telemetry-push` fall short of the rest of the specification, in two different ways:

1. **Malformed Pub/Sub envelope** (invalid JSON body, missing `message`, invalid base64 in `message.data`): the behaviour **is decided** — [ADR-0002](../adr/0002-event-driven-pubsub-push-to-cloud-run.md) requires HTTP `400 Bad Request` and no Firestore write. V1 only **defers the scenario** that would enforce it; only missing fields inside a valid envelope are executed.
2. **Unknown zone** (no document `geofences/<zone>`): the behaviour **is not decided**. No ADR fixes the HTTP status or whether operators are notified.

## Context

The error path enumeration ([`bdd/00_error_path_enumeration.md`](../../bdd/00_error_path_enumeration.md), rows 2.4 and 2.5) lists both cases. In V1, operators seed `geofences/<zone>` before a collar is activated, and the outer envelope is produced by the managed Pub/Sub service, not by clients.

## Nature of the weakness

- **Malformed envelope:** an implementation that answers anything but `400` violates ADR-0002, but no scenario would catch it.
- **Unknown zone:** an implementation may reject, drop or accept the ping; none of these is wrong in V1, and none is guaranteed.

## Why the clean solution is not chosen

- The envelope scenario needs crafted Pub/Sub push bodies for MI2, MI3 and MI4; V1 keeps the HTTP scenarios to valid envelopes with and without mandatory fields.
- The unknown-zone case needs an operator-facing decision (silently drop, reject with `4xx`, or alert operators) that V1 does not have. Specifying a status code now would freeze a behaviour nobody has decided.

## Mitigations in place

1. ADR-0002 states the required `400` for malformed envelopes, so an implementing agent has a binding rule even without a scenario.
2. Rows 2.4 and 2.5 of the error path enumeration are marked `none` with this LIM as the reason.
3. An AI agent reading this LIM knows the unknown-zone behaviour is open and must not present any choice as specified.

## Residual risk

A corrupted envelope may be answered with a status other than `400` without any test failing; a ping for a zone that was never seeded may be rejected, dropped or retried by Pub/Sub depending on the implementation.

## Triggers for revisit

- Operator alerting for misconfigured collars (decide the unknown-zone behaviour, then specify it).
- Clients other than the managed Pub/Sub push subscription (add the envelope scenario).

## References

- [ADR-0002](../adr/0002-event-driven-pubsub-push-to-cloud-run.md)
- [ADR-0003](../adr/0003-firestore-persistence-and-alert-schema.md)
- [`bdd/00_error_path_enumeration.md`](../../bdd/00_error_path_enumeration.md)
