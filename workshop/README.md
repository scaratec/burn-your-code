# Workshop: EquiGuard – AI-Driven Geofencing & Event-Driven Architecture

## About the Project

This project is the hands-on workshop for the presentation
**"Burn Your Code: Feature Files as the Ultimate AI Agent Prompt"**.
We build a high-precision, event-driven geofencing system on Google Cloud
where the entire business logic and infrastructure configuration are driven
exclusively by **Gherkin Feature Files**.

### The Case: "EquiGuard Dreilingen"

We monitor the pasture areas in Dreilingen (Heidewiese). Using GPS telemetry,
the system determines in real-time whether horses (e.g., Lilly or Honey) have
left the predefined geofence.

---

## Architecture

The system follows **Ports & Adapters (Hexagonal Architecture)**:

```
GPS Telemetry
     │
     ▼
Pub/Sub Topic (equiguard-telemetry)
     │
     ▼ push subscription
Cloud Run: geofence-processor
     │  reads geofence polygon
     ├──────────────────────► Firestore (geofences/)
     │  writes alert on violation
     └──────────────────────► Firestore (alerts/)
```

---

## Milestones

The workshop is structured in four milestones of increasing complexity.
Each milestone uses the same Gherkin feature files — only the execution
environment changes.

### MI1 — Geofence Library (`@mi1`)

Tests the core point-in-polygon algorithm in isolation. No network, no
services. The Python step code calls a Go CLI wrapper via subprocess.

```bash
make test-mi1
```

Requirements: Go 1.22+, Python 3.11+

---

### MI2 — Geofence Processor with Emulators (`@mi2`)

Tests the full HTTP service locally using the **Firestore emulator** and
**Pub/Sub emulator**. Emulators are started and stopped automatically.

```bash
make test-mi2
```

`make test-mi2` starts both emulators, runs the scenarios, and stops
everything — even on failure.

To manage emulators manually:

```bash
make start-emulators   # Firestore on :8082 (npx firebase-tools), Pub/Sub on :8085 (Docker)
make stop-emulators    # stop and remove all emulators
```

**Emulator requirements:**
- Firestore: Node.js 18+ with `npx` (firebase-tools downloads the JAR on first run)
- Pub/Sub: Docker + `gcr.io/google.com/cloudsdktool/cloud-sdk:latest`

Requirements: MI1 + Node.js 18+ + Docker

---

### MI3 — OCI Image (`@mi3`)

Builds the geofence-processor Docker image and tests it as a running
container. Validates health check, port binding, and full behavioural
equivalence with MI2.

```bash
make test-mi3
```

Requirements: MI2 + Docker

---

### MI4 — Cloud Run on Live GCP (`@mi4`)

> **⚠ WARNING: This milestone uses real GCP resources and incurs costs.**
> It is intended for use with Google Cloud credits provided for this workshop.
> Always run `make teardown-mi4` after the session to stop billing.

This is where it gets real. The same Gherkin scenarios that passed locally
in MI1–MI3 now run against a live Cloud Run service, real Firestore, and
real Pub/Sub — without changing a single line of the feature file.

#### Prerequisites

| Requirement | How to verify |
|---|---|
| GCP project `randy-gupta-poc` with billing enabled | `gcloud projects describe randy-gupta-poc` |
| Application Default Credentials | `gcloud auth application-default login` |
| Terraform ≥ 1.7 | `terraform version` |
| Docker authenticated for Artifact Registry | `make auth-registry` |
| MI3 image built locally | `docker images equiguard/geofence-processor:test` |

#### Required GCP APIs

The following APIs must be enabled (Terraform handles this automatically):

- `run.googleapis.com`
- `pubsub.googleapis.com`
- `firestore.googleapis.com`
- `artifactregistry.googleapis.com`

#### Step-by-Step

```bash
# 1. Provision all GCP resources and deploy the image in one step:
#    - Phase 1: creates the Artifact Registry repository
#    - pushes the container image
#    - Phase 2: deploys Cloud Run, Pub/Sub topic + push subscription
make tf-apply

# 2. Run the MI4 BDD tests against the live service
make test-mi4
```

#### What Terraform provisions

| Resource | Name | Description |
|---|---|---|
| Artifact Registry | `equiguard` | Docker repository for container images |
| Cloud Run | `geofence-processor` | HTTP service, region `europe-west3` |
| Pub/Sub Topic | `equiguard-telemetry` | Receives GPS telemetry events |
| Pub/Sub Subscription | `equiguard-telemetry-push-sub` | Push → Cloud Run `/telemetry-push` |

All values are defined in `terraform/terraform.tfvars` and mirrored in the
Gherkin Background table — no magic values anywhere.

#### Teardown

Run this after the workshop to destroy all GCP resources and stop billing:

```bash
make teardown-mi4
```

This runs `terraform destroy` and requires manual confirmation.

---

## Guardrails Against Hallucination

- **No Magic Values:** All ports, IBANs, coordinates, and env vars are
  explicit in the Gherkin file (BDD Guideline 2.1).
- **Eventual Consistency:** Assertions use polling with deadlines instead
  of fixed sleeps (BDD Guideline 6.4).
- **Behavioural Equivalence:** MI4 uses the identical payloads as MI2/MI3.
  If MI4 fails where MI2 passes, the problem is infrastructure — not logic.
- **Test Isolation:** Firestore data is cleared after each scenario in all
  milestones (emulator bulk-delete for MI1–MI3, document-level delete for MI4).

---

*Created for the presentation: Burn Your Code – Feature Files as the
Ultimate AI Agent Prompt.*
