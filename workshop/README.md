# Hands-On Workshop: EquiGuard — Specification-First Engineering with Antigravity CLI, Gemini & Google Cloud

## Goal of the Workshop

In this workshop, you will build **EquiGuard** — a real-time, event-driven GPS pasture monitoring system on Google Cloud — without writing a single line of application code by hand.

Instead of "Vibe Coding" (ad-hoc chat prompting that builds a fragile house of cards), you will use **Antigravity CLI (`agy`)** and **Gemini** to engineer a **complete, self-verifying specification triad**:

1. **ADRs (`governance/adr/`)** — *Why* the system is built this way.
2. **LIMs (`governance/limitations/`)** — *Where* V1 knowingly accepts bounded shortcuts.
3. **Gherkin Feature Files (`bdd/*.feature`) & Black-Box Steps (`bdd/steps/`)** — *What* the system does observably from the outside.

Once your specification passes the **Specification Critic (`bdd-critic`)** and your black-box test suite is **cleanly RED**, you will pick **any programming language you like** (Go, Python, Rust, TypeScript, Java…) and watch **Gemini** generate the entire service autonomously until every milestone is **GREEN** — locally and live on **Google Cloud Run**.

---

## The Use Case: "EquiGuard"

We monitor horse pastures using GPS collar telemetry. Whenever a horse (e.g., *Lilly* or *Honey*) sends a GPS ping, EquiGuard determines via ray casting whether the coordinate lies inside or outside the assigned pasture polygon (`HomePasture` or `ComplexPasture`) and writes a `GEOFENCE_VIOLATION` alert to Firestore when a horse leaves the pasture.

*(Note: Polygon coordinates, horse names, and project IDs in this workshop are intentional decoy data picked from Google Maps so the workshop ships with realistic values without exposing real-world locations.)*

```text
GPS Telemetry
     │
     ▼
Pub/Sub Topic (equiguard-telemetry)
     │
     ▼ push subscription (POST /telemetry-push)
Cloud Run: geofence-processor
     │  reads geofence polygon
     ├──────────────────────► Firestore (geofences/<zone>)
     │  writes alert on violation
     └──────────────────────► Firestore (alerts/<doc>)
```

---

## The Five Development Phases

We follow the exact 5-phase engineering cycle from the slides ([`AGENTS.md`](AGENTS.md) & [BDD Guidelines v1.9.0](../BDD_GUIDELINES_v1.9.0_EN.md)):

```text
  Phase 1: Dialogue & ADRs/LIMs   →  governance/adr/ + governance/limitations/  (WHY / WHERE NOT)
  Phase 2: Error Paths & Features →  bdd/00_error_path_enumeration.md + *.feature (WHAT — RED)
  Phase 3: Specification Critic   →  Whole-picture review of Phases 1 + 2       (AUDITED)
  Phase 4: Steps & Honesty Audit  →  bdd/steps/*_steps.py + §13 Step Audit      (STILL RED)
  Phase 5: Code & Cloud Rollout   →  Autonomous build in ANY language + GCP MI4 (GREEN)
```

> **The Feedback Loop Rule:** Whatever the Critic (Phase 3), the Step Audit (Phase 4), or Reality (Phase 5) finds modifies the **ADR, LIM, or Feature File first** — never directly the application code.

---

## Quick Prerequisites & Setup

```bash
# Install Python BDD virtual environment (.venv)
make setup
```

### Phase Checkpoints (Jump In Anywhere!)

This repository includes checkpoint targets in the `Makefile` so you can start from scratch at Phase 1 **or** fast-forward to any phase if time gets tight during the workshop:

| Command | What It Prepares |
|---|---|
| `make phase1-start` | Blank slate: keeps only `AGENTS.md`, `GEMINI.md`, `governance/*/TEMPLATE.md`, `geofence.kml`, and `terraform/`. Ready to start **Phase 1**. |
| `make checkpoint-adrs` | Restores the reference ADRs (`0000`–`0004`) and LIMs (`0001`–`0002`). Ready to start **Phase 2**. |
| `make checkpoint-features` | Restores reference ADRs, LIMs, `00_error_path_enumeration.md`, and `.feature` files. Ready for **Phase 3 & 4**. |
| `make burn` | Restores reference ADRs, LIMs, Feature Files, and language-neutral Step Files, and deletes all application code. Ready for **Phase 5 (Autonomous Polyglot Implementation)**. |
| `make restore-all` | Restores the complete reference workspace including the reference Go implementation. |

---

## Step-by-Step Workshop Guide

### Phase 0: Kickoff Video — Autonomous Rebuild from Zero Code

Before writing anything, we watch the timelapse run: starting from **0 lines of application code** and a read-only specification (`governance/` + `bdd/`), a single prompt drives the agent to implement `geofence-lib-test`, `geofence-processor`, and `Dockerfile` until `make test-all` passes twice in a row.

*(See [`../video-demo/README.md`](../video-demo/README.md) for the recording and assembly pipeline used to produce the workshop video.)*

---

### Phase 1: Architecture Dialogue → ADRs & LIMs (`governance/`)

1. Reset the workspace to the Phase 1 starting state:
   ```bash
   make phase1-start
   ```
2. Launch **Antigravity CLI (`agy`)** with Gemini and run the prompt in [`prompts/01-architecture-dialogue.md`](prompts/01-architecture-dialogue.md).
3. Guided by [`GEMINI.md`](GEMINI.md) and [`AGENTS.md`](AGENTS.md), the agent asks **one architectural question at a time** (with options, a recommendation, and consequences — leaving the programming language open!).
4. Review the generated files under `governance/adr/` (`0001`–`0004`) and `governance/limitations/` (`0001`–`0002`).

*(Short on time? Run `make checkpoint-adrs` to load the reference ADRs and LIMs.)*

---

### Phase 2: Error Path Enumeration & Gherkin Feature Files (`bdd/`)

1. In **Antigravity CLI (`agy`)**, run the prompt in [`prompts/02-error-paths-and-features.md`](prompts/02-error-paths-and-features.md).
2. First, the agent creates [`bdd/00_error_path_enumeration.md`](bdd/00_error_path_enumeration.md) (BDD Guidelines §4.5: quantifying failure paths layer by layer before writing scenarios).
3. Next, it drafts the four progressive milestone feature files:
   - **`bdd/mi1_geofence_library.feature` (`@mi1`):** Point-in-polygon algorithm in isolation (`HomePasture` convex + `ComplexPasture` concave).
   - **`bdd/mi2_geofence_processor.feature` (`@mi2`):** Local HTTP service with Firestore (`:8082`) and Pub/Sub (`:8085`) emulators (`Lilly` outside → alert; `Honey` inside → no alert).
   - **`bdd/mi3_geofence_processor_image.feature` (`@mi3`):** OCI container image (`GET /health`, port `8081`, behavioral equivalence, plus `Scenario Outline` for HTTP `400` on missing mandatory fields).
   - **`bdd/mi4_cloud_run.feature` (`@mi4`):** Live Cloud Run + real Pub/Sub + real Firestore (`project_id` in Background table as single source of truth).

---

### Phase 3: The Specification Critic (`bdd-critic`)

Before a single line of Python step code or application code exists, we audit the specification as a whole (BDD Guidelines §14):

1. Start a fresh **Antigravity CLI (`agy`)** session and run [`prompts/03-spec-critic.md`](prompts/03-spec-critic.md).
2. The Critic reads **only Markdown and Gherkin** (`governance/adr/*.md`, `governance/limitations/*.md`, `bdd/00_error_path_enumeration.md`, `bdd/*.feature`) and checks all six edges:
   - Binding set & statuses
   - Record vs. Record contradictions
   - Feature vs. Feature consistency across MI1–MI4
   - ADR ↔ Feature File & Error Path coverage
   - LIM coverage of deliberate V1 simplifications
   - Scenario honesty (can `Then` fail? are negative controls present?)
3. Resolve any findings in the ADRs, LIMs, or `.feature` files.

*(Short on time? Run `make checkpoint-features` to load the audited reference specification.)*

---

### Phase 4: Language-Neutral Step Definitions & Step Honesty Audit (`bdd/steps/`)

1. Run [`prompts/04a-step-definitions.md`](prompts/04a-step-definitions.md) in **Antigravity CLI (`agy`)** to generate the black-box Python `behave` steps (`bdd/steps/`) and cleanup hooks (`bdd/environment.py`).
   - Notice how the steps are **100% language-neutral** ([ADR-0004](governance/adr/0004-language-neutral-black-box-test-harness.md)): MI1 talks `stdin`/`stdout` JSON to `./bin/geofence-lib-test`, MI2 runs `./bin/geofence-processor` over HTTP + Firestore emulator, MI3 runs the Docker container, and MI4 talks to GCP.
2. Run the independent **Step Honesty Audit** (BDD Guidelines §13) using [`prompts/04b-step-honesty-audit.md`](prompts/04b-step-honesty-audit.md) to verify:
   - **Check 1:** Independent channel verification (reading Firestore directly, never trusting HTTP 200 alone).
   - **Check 2:** Origin analysis for all `Then` values.
   - **Check 3:** Data symmetry (zero hidden business logic or fabricated defaults in Python steps).
3. Verify that the suite runs and fails **cleanly RED**:
   ```bash
   make test-mi1
   ```

---

### Phase 5: Autonomous Polyglot Code Generation & GCP Rollout (`GREEN` + `MI4`)

Now comes the payoff!

1. Ensure your workspace contains **only** the specification and steps (no application code):
   ```bash
   make burn
   ```
2. Choose **any programming language you want** — **Python**, **Go**, **Rust**, **TypeScript/Node.js**, **Java** — and launch **Antigravity CLI (`agy`)** with Gemini using [`prompts/05-autonomous-implementation.md`](prompts/05-autonomous-implementation.md):
   ```bash
   # Example interactive or headless run with Antigravity CLI:
   agy --model gemini-4-argon-high
   ```
3. Watch Gemini implement the CLI (`./bin/geofence-lib-test`), the HTTP service (`./bin/geofence-processor`), and the `Dockerfile`, and iterate autonomously against the local emulators until `make test-all` passes **twice in a row**!

```bash
make test-mi1   # Milestone 1: Core algorithm via CLI
make test-mi2   # Milestone 2: HTTP processor + Firestore/PubSub emulators
make test-mi3   # Milestone 3: OCI Docker container + emulators
make test-all   # Run MI1 + MI2 + MI3
```

---

### Bonus: Milestone 4 — Live Deployment on Google Cloud Run (`@mi4`)

> **⚠ WARNING: Milestone 4 provisions real GCP resources and incurs costs.**
> Always run `make teardown-mi4` after the session to destroy all cloud resources.

The exact same Gherkin scenarios that passed locally in MI2 and MI3 now run against live **Google Cloud Run**, real **Firestore**, and real **Pub/Sub**:

1. **One edit in the specification:** Open `bdd/mi4_cloud_run.feature` and change `project_id` in the `Background` table to your GCP project ID. (The `Makefile` extracts `project_id` from there automatically and passes it to Docker and Terraform — zero duplicate config files!)
2. **Ensure GCP authentication:**
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```
3. **Provision & Deploy via Terraform:**
   ```bash
   make tf-apply
   ```
4. **Run the live Cloud Run BDD suite:**
   ```bash
   make test-mi4
   ```
5. **Teardown after the workshop:**
   ```bash
   make teardown-mi4
   ```
