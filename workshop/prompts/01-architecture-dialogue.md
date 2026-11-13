# Phase 1 Prompt — Architecture Dialogue (ADRs & LIMs)

Run this prompt in **Antigravity CLI (`agy`)** with Gemini after running `make phase1-start`:

```text
We want to build "EquiGuard", a real-time GPS pasture geofencing service for horses on Google Cloud.

Read AGENTS.md, governance/README.md, governance/adr/TEMPLATE.md, and governance/limitations/TEMPLATE.md first.

Follow Stage 1 and Stage 2 of AGENTS.md strictly:
1. Conduct the architecture dialogue with me ONE question at a time (never multiple questions in one message). For each question, state the options, your recommendation with a one-sentence reason, and the consequences.
2. Cover these four architectural decisions:
   - ADR-0001: Point-in-polygon algorithm (ray casting vs. winding number vs. external GIS library) for convex and concave polygons (geofence.kml).
   - ADR-0002: Event-driven ingestion and runtime on GCP (Pub/Sub push subscription -> Cloud Run HTTP service with GET /health and POST /telemetry-push, returning HTTP 400 on missing mandatory fields).
   - ADR-0003: Persistence & schema in Firestore (collections `geofences` for polygon master data and `alerts` for `GEOFENCE_VIOLATION` records).
   - ADR-0004: Language-neutral black-box BDD test harness in Python `behave` across 4 milestones (MI1 CLI stdin/stdout JSON, MI2 local HTTP + emulators, MI3 OCI container image, MI4 live Cloud Run via Terraform).
3. Keep the specification 100% language-neutral — do not lock in the application programming language yet.
4. After the dialogue, write ADR-0001 through ADR-0004 under `governance/adr/`, record deliberate V1 simplifications (single static polygon per pasture; stateless per-ping evaluation without deduplication) as LIM-0001 and LIM-0002 under `governance/limitations/`, and update both README index tables.
```
