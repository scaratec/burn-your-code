# Burn Your Code — hands-on workshop: EquiGuard

In this workshop you change the behaviour of a service **without writing a single line of application code by hand**. You decide, you specify, an independent critic audits the specification — and then an AI agent rebuilds the code from the specification alone, in a programming language of your choice.

The system is **EquiGuard**: GPS collars on horses send pings, and the service decides whether a horse is still inside its pasture polygon.

```text
GPS ping {"lon", "lat", "zone"} ──► geofence-processor ──► alert if the horse is outside the pasture
                                     └─ geofence library (milestone 1: ./bin/geofence-lib-test)
```

## The 90-minute workshop

| | |
|---|---|
| Preparation (at home, 15 min) | [`PREPARATION.md`](PREPARATION.md), finish with `make check` |
| Exercises | [`exercises/README.md`](exercises/README.md) — four exercises around one question: *a horse stands exactly on the fence — inside or outside?* |
| Tools | Python 3.11+, the Antigravity CLI (`agy`) with **Gemini 3.8 Flash (High)** |
| Slides | [`../facilitator/slides/index.html`](../facilitator/slides/index.html) (offline) and [`../facilitator/slides/deck.pdf`](../facilitator/slides/deck.pdf) |
| Facilitators | [`../facilitator/FACILITATOR.md`](../facilitator/FACILITATOR.md) — timing, reference solutions, troubleshooting |

All four exercises run locally against **milestone 1** (the geofence library as a small CLI). No Docker, no cloud account.

## What is in this directory

| Path | Contents |
|---|---|
| [`AGENTS.md`](AGENTS.md) | Binding charter for every coding agent working here |
| [`governance/adr/`](governance/adr/) | Architecture Decision Records — *why* |
| [`governance/limitations/`](governance/limitations/) | Limitation Records — *where not (yet)* |
| [`bdd/`](bdd/) | Error path enumeration, feature files (*what*) and language-neutral black-box steps |
| [`exercises/`](exercises/) | The four workshop exercises and the bonus, each with a `PROMPT.md` |
| [`prompts/`](prompts/) | Prompts for the full five-phase cycle (going further) |
| `cmd/`, `internal/`, `Dockerfile` | Reference implementation in Go (milestones 2–4) |
| [`terraform/`](terraform/) | Cloud Run, Pub/Sub and Firestore for milestone 4 |

## The specification triad and the five phases

```text
  Phase 1: Decisions               →  governance/adr/ + governance/limitations/   (WHY / WHERE NOT)
  Phase 2: Error paths & features  →  bdd/00_error_path_enumeration.md + *.feature (WHAT — RED)
  Phase 3: Specification critic    →  whole-picture review of phases 1 + 2        (AUDITED)
  Phase 4: Steps & honesty audit   →  bdd/steps/*_steps.py + §13 step audit       (STILL RED)
  Phase 5: Implementation          →  autonomous build in any language            (GREEN)
```

> **Feedback loop rule:** whatever gap in the specification the critic, the step audit or reality reveals changes the ADR, LIM or feature file first — never the application code directly. Code that fails an existing scenario is a bug and is fixed in the code.

The guidelines behind it: [BDD Guidelines v1.9.0](BDD_GUIDELINES_v1.9.0_EN.md) ([Deutsch](BDD_GUIDELINES_v1.9.0_DE.md)).

---

## Going further

### The full five-phase cycle (self-study, half a day)

Build the whole EquiGuard specification from scratch, phase by phase. Each phase has a prompt in [`prompts/`](prompts/) and a checkpoint, so you can jump in anywhere:

| Command | Prepares |
|---|---|
| `make phase1-start` | Blank slate: only `AGENTS.md`, templates, `geofence.kml` and `terraform/` remain. Start with [`prompts/01-architecture-dialogue.md`](prompts/01-architecture-dialogue.md). |
| `make checkpoint-adrs` | Reference ADRs 0000–0004 and LIMs 0001–0002 — ready for phase 2 ([`prompts/02-error-paths-and-features.md`](prompts/02-error-paths-and-features.md)) |
| `make checkpoint-features` | Plus error paths and feature files — ready for phases 3 and 4 ([`03`](prompts/03-spec-critic.md), [`04a`](prompts/04a-step-definitions.md), [`04b`](prompts/04b-step-honesty-audit.md)) |
| `make burn` | Plus steps; all application code deleted — ready for phase 5 ([`prompts/05-autonomous-implementation.md`](prompts/05-autonomous-implementation.md)) |
| `make restore-all` | The complete reference workspace including the Go implementation |

`phase1-start` and `burn` delete files. Commit or copy your own work first.

### Milestones 2–4

| Milestone | Tag | Verifies | Needs |
|---|---|---|---|
| MI1 | `@mi1` | point-in-polygon library via CLI (`stdin`/`stdout` JSON) | Python |
| MI2 | `@mi2` | HTTP service `geofence-processor`: Pub/Sub push → Firestore | Go (reference build), Node.js, **Java 21+** (Firestore emulator) |
| MI3 | `@mi3` | OCI image: health check, port, HTTP 400 validation, same behaviour as MI2 | as MI2, plus Docker on Linux (the container uses host networking) |
| MI4 | `@mi4` | live on Cloud Run with real Pub/Sub and Firestore, provisioned by Terraform | a GCP project, `gcloud`, Terraform |

```bash
make restore-all      # reference implementation in Go
make test-mi2         # starts and stops the Firestore emulator on :8082
make test-mi3         # builds equiguard/geofence-processor:test
make test-all         # MI1 + MI2 + MI3
```

**Milestone 4 provisions real GCP resources and incurs costs.** The project ID has a single source of truth: the `project_id` row in the `Background` table of [`bdd/mi4_cloud_run.feature`](bdd/mi4_cloud_run.feature).

```bash
gcloud auth login && gcloud auth application-default login
make tf-apply         # Artifact Registry, image push, Cloud Run, Pub/Sub
make test-mi4
make teardown-mi4     # destroy everything afterwards
```
