# Limitation Records (LIMs)

This directory contains the Limitation Records for **EquiGuard**, documenting deliberate, bounded V1 simplifications against our ADRs and requirements. Every record follows [`TEMPLATE.md`](TEMPLATE.md).

## Index

| LIM | Title | Status | Intent | Related ADRs |
|---|---|---|---|---|
| [LIM-0001](0001-single-static-polygon-per-pasture.md) | V1 supports a single static polygon per pasture without interior exclusion zones | Accepted | must-resolve | [ADR-0001](../adr/0001-point-in-polygon-ray-casting.md), [ADR-0003](../adr/0003-firestore-persistence-and-alert-schema.md) |
| [LIM-0002](0002-stateless-per-ping-evaluation-without-deduplication.md) | V1 evaluates each ping statelessly without state-transition tracking or deduplication | Accepted | must-resolve | [ADR-0002](../adr/0002-event-driven-pubsub-push-to-cloud-run.md), [ADR-0003](../adr/0003-firestore-persistence-and-alert-schema.md) |
| [LIM-0003](0003-unknown-zone-unspecified-malformed-envelope-untested.md) | V1 leaves unknown zones unspecified and malformed Pub/Sub envelopes untested | Accepted | must-resolve | [ADR-0002](../adr/0002-event-driven-pubsub-push-to-cloud-run.md), [ADR-0003](../adr/0003-firestore-persistence-and-alert-schema.md) |
