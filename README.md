# Burn Your Code: Specification-First Engineering for Autonomous AI Agents

This repository contains the guidelines, governance framework, slide deck, video demo pipeline, and hands-on workshop for **AI-Native Specification-First Engineering** with **Antigravity CLI (`agy`)**, **Google Gemini**, and **Behavior-Driven Development (BDD)**.

---

## The Core Concept: From House of Cards to Foundation

AI agents write code faster than humans make decisions. When teams rely on ad-hoc chat prompting (**"Vibe Coding"**), every generated file leans on unwritten assumptions. Because agents have no memory across sessions, anything not written down in the repository is re-negotiated or hallucinated on the next prompt.

This project demonstrates the **95 / 5 Shift**:
- **95% Understand, Define, and Validate the Problem** in a three-register specification triad (**ADRs + LIMs + Gherkin Feature Files**), audited as a whole by an independent **Specification Critic (`bdd-critic`)** and backed by language-neutral **Black-Box Steps**.
- **5% Implement with AI:** Once the specification is complete and read-only, **Gemini** (via **Antigravity CLI**) generates the entire application autonomously in **any programming language** (Go, Python, Rust, TypeScript, Java…) until every BDD milestone passes. Application code becomes a disposable, replaceable build artifact.

---

## The Five-Phase Development Cycle

```text
  Phase 1: Architecture Dialogue  →  governance/adr/ + governance/limitations/  (WHY / WHERE NOT)
  Phase 2: Error Paths & Features →  bdd/00_error_path_enumeration.md + *.feature (WHAT — RED)
  Phase 3: Specification Critic   →  Whole-picture review of Phases 1 + 2       (AUDITED)
  Phase 4: Steps & Honesty Audit  →  bdd/steps/*_steps.py + §13 Step Audit      (STILL RED)
  Phase 5: Code & Cloud Rollout   →  Autonomous build in ANY language + GCP MI4 (GREEN)
```

> **The Feedback Loop Rule:** Whatever the Specification Critic (Phase 3), the Step Honesty Audit (Phase 4), or Reality (Phase 5) finds modifies the **ADR, LIM, or Feature File first** — never directly the application code.

---

## Hands-On Workshop (`/workshop`)

The [`/workshop`](./workshop/) directory contains the complete hands-on workshop:

**EquiGuard — Event-Driven GPS Pasture Geofencing on Google Cloud**

Participants use **Antigravity CLI (`agy`)** and **Gemini** to walk through all five phases:
1. Conduct the guided architecture dialogue (`prompts/01-architecture-dialogue.md`) to create **ADRs 0000–0004** and **LIMs 0001–0002**.
2. Enumerate all 15 error paths (`bdd/00_error_path_enumeration.md`) and write the four Gherkin feature files (`prompts/02-error-paths-and-features.md`).
3. Audit the specification as a whole with the **Specification Critic** (`prompts/03-spec-critic.md`).
4. Generate language-neutral black-box Python `behave` steps (`prompts/04a-step-definitions.md`), audit them for test honesty (`prompts/04b-step-honesty-audit.md`), and verify the **RED** state.
5. Run `make burn`, pick **any programming language**, and let Gemini autonomously implement the service (`prompts/05-autonomous-implementation.md`) until all milestones pass — locally and on live **Google Cloud Run**!

| Milestone | Tag | What It Verifies | Environment |
|---|---|---|---|
| **MI1** | `@mi1` | Point-in-polygon ray-casting algorithm (`HomePasture` convex + `ComplexPasture` concave) | CLI (`stdin`/`stdout` JSON), no network |
| **MI2** | `@mi2` | HTTP `geofence-processor` service + Pub/Sub push ingestion + Firestore persistence | Local Firestore (`:8082`) & Pub/Sub (`:8085`) emulators |
| **MI3** | `@mi3` | Containerized OCI image (`GET /health`, port `8081`, HTTP `400` validation, behavioral equivalence) | Docker + local emulators |
| **MI4** | `@mi4` | Live production deployment provisioned via Terraform (`project_id` read from Gherkin!) | Real GCP Cloud Run, Pub/Sub & Firestore |

See [`/workshop/README.md`](./workshop/README.md) for the step-by-step participant guide and `Makefile` phase checkpoints (`make phase1-start`, `make checkpoint-adrs`, `make checkpoint-features`, `make burn`, `make restore-all`).

---

## BDD Guidelines v1.9.0 & Governance Triad

- **BDD Guidelines v1.9.0:**
  - English: [`BDD_GUIDELINES_v1.9.0_EN.md`](./BDD_GUIDELINES_v1.9.0_EN.md)
  - German: [`BDD_GUIDELINES_v1.9.0_DE.md`](./BDD_GUIDELINES_v1.9.0_DE.md)
  - Includes §3.4 (Verifying Configuration Data), §4.5 (Systematic Error Path Enumeration), §4.6 (Domain Signals in Feature Files), §13 (Step Honesty Spec-Audit), and §14 (Pre-Code Specification Critic `bdd-critic`).
- **Companion Governance Framework (`/governance`):**
  - Overview: [`governance/README.md`](./governance/README.md)
  - Architecture Decision Records (ADRs): [`governance/adr/`](./governance/adr/)
  - Limitation Records (LIMs): [`governance/limitations/`](./governance/limitations/)

---

## Repository Structure

- **[`/workshop`](./workshop/)**: Hands-on 5-phase BDD & ADR workshop with Antigravity CLI prompts, language-neutral harness, and 4 GCP milestones.
- **[`/slides`](./slides/)**: Standalone offline **Reveal.js HTML deck** ([`slides/index.html`](./slides/index.html)) plus companion Markdown slide cards (`01`–`19`).
- **[`/video-demo`](./video-demo/)**: Recording (`tmux` + live dashboard) and `ffmpeg` assembly pipeline for the autonomous rebuild kickoff video.
- **[`/governance`](./governance/)**: ADR + LIM templates and framework documentation.
- **[`submission_data.md`](./submission_data.md)**: Rethought title options, elevator pitch, abstracts (EN/DE), key takeaways, and workshop outline.
