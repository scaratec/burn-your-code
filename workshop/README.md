# Workshop: EquiGuard – AI-Driven Geofencing & Event-Driven Architecture

## About the Project

This project is the hands-on workshop for the presentation
**"Burn Your Code: Feature Files as the Ultimate AI Agent Prompt"**.
We build a high-precision, event-driven geofencing system on Google Cloud
where the entire business logic and infrastructure configuration are driven
exclusively by **Gherkin Feature Files**.

### The Case: "EquiGuard"

We monitor the pasture areas in Lower Saxony. Using GPS telemetry,
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

## Setup

```bash
make setup
```

This single command:
1. Creates a Python virtual environment (`.venv/`)
2. Installs all Python dependencies from `requirements.txt` with **pinned
   versions** — every participant gets the exact same library stack
3. Resolves Go module dependencies (`go mod tidy`)
4. Creates the `bin/` directory for compiled binaries

`make test-mi4` uses `make setup-python` instead of `make setup` — it
only installs Python dependencies because MI4 does not need Go binaries.

### Upgrading Python dependencies

Dependencies are pinned in `requirements.txt` at the patch level. To upgrade:

```bash
# Edit requirements.txt with new version pins, then:
make setup
make test-all   # verify all local milestones still pass
# commit requirements.txt
```

For a fully locked environment including all transitive dependencies:

```bash
pip install pip-tools
pip-compile requirements.txt -o requirements.lock.txt
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
- Firestore: Node.js 18+ with `npx`. The Makefile pins
  `firebase-tools@15.11.0` — the JAR is downloaded on first run and
  cached by npx. Pinning the version guarantees the same emulator
  behaviour across all workshop runs.
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

#### Participant setup — one edit required

Open `bdd/mi4_cloud_run.feature` and change the `project_id` value in
the Background table to your GCP project ID. That is the **only file
you need to edit**: the Makefile reads `project_id` from there via
`awk` and derives the Artifact Registry image URL and all Terraform
`-var` flags automatically. No other configuration file is touched.

#### Prerequisites

| Requirement | How to verify |
|---|---|
| GCP project with billing enabled | `gcloud projects describe <project_id>` |
| Application Default Credentials | `gcloud auth application-default login` |
| Terraform ≥ 1.7 | `terraform version` |
| Docker authenticated for Artifact Registry | `make auth-registry` |

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

`make test-mi4` performs two preflight checks before launching Behave:

1. **Terraform outputs** — verifies that `terraform output cloud_run_url`
   succeeds. If not, the run is aborted with the message
   `Run 'make tf-apply' before 'make test-mi4'`.
2. **gcloud credentials** — verifies that `gcloud auth print-identity-token`
   succeeds. If not, the run is aborted with the instruction
   `Run: gcloud auth application-default login`.

> **Design note:** The Gherkin step `And the infrastructure is provisioned
> with Terraform` reads Terraform outputs only — it does **not** run
> `terraform apply`. Provisioning is a deployment concern handled by
> `make tf-apply`; a Given step describes world state, it does not change it.

#### What Terraform provisions

| Resource | Name | Description |
|---|---|---|
| Artifact Registry | `equiguard` | Docker repository for container images |
| Cloud Run | `geofence-processor` | HTTP service, region `europe-west3` |
| Pub/Sub Topic | `equiguard-telemetry` | Receives GPS telemetry events |
| Pub/Sub Subscription | `equiguard-telemetry-push-sub` | Push → Cloud Run `/telemetry-push` |

All values are defined in `terraform/terraform.tfvars` and mirrored in the
Gherkin Background table — no magic values anywhere.

#### Terraform state

By default Terraform stores state locally in `terraform/terraform.tfstate`
(excluded from version control). This works fine for a single operator.

For **team use**, configure a shared GCS backend so all members operate on
the same state file. Instructions are in the commented `backend "gcs"` block
at the top of `terraform/main.tf`.

The provider lock file `terraform/.terraform.lock.hcl` **is** tracked in
version control. It pins the exact `hashicorp/google` provider version
(currently `5.45.2`) so participants do not depend on the Terraform registry
being available or returning a different version during the workshop.

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
- **Test Isolation:** Firestore data is cleared after each scenario in
  `bdd/environment.py`. MI2/MI3 use a single HTTP DELETE against the
  emulator API (atomic, fast). MI4 streams and deletes documents
  individually from real Firestore, touching only the `alerts` and
  `geofences` collections.

---

*Created for the presentation: Burn Your Code – Feature Files as the
Ultimate AI Agent Prompt.*
