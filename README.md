# Burn Your Code: Specification-First Engineering for Autonomous AI Agents

This repository contains the guidelines, governance framework, talk deck, and hands-on workshop for **AI-Native Specification-First Engineering** with **Antigravity CLI (`agy`)**, **Google Gemini**, and **Behavior-Driven Development (BDD)**.

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

> **The Feedback Loop Rule:** Whatever gap or contradiction in the specification the Specification Critic (Phase 3), the Step Honesty Audit (Phase 4), or Reality (Phase 5) reveals modifies the **ADR, LIM, or Feature File first** — never directly the application code. Code that merely fails an existing scenario is a bug and is fixed in the code.

---

## Hands-On Workshop (`/workshop`)

**90 minutes, four exercises, one question: a horse stands exactly on the fence — inside or outside?**

The [`/workshop`](./workshop/) directory contains a ready-to-run workshop around **EquiGuard**, a GPS pasture geofencing service. Participants use the **Antigravity CLI (`agy`)** with **Gemini 3.8 Flash** and never write application code by hand:

| # | Exercise | Phase |
|---|---|---|
| 1 | Decide the fence: an architecture dialogue produces ADR-0005 and LIM-0004 | Decisions |
| 2 | Make it red: error paths first, then boundary scenarios | Error paths & feature files |
| 3 | Let the critic find the bugs: five defects hidden in the specification | Specification critic |
| 4 | Burn your code: delete all code, rebuild it in any language until green | Autonomous implementation |
| + | Can the tests cheat? A dishonest step file | Step honesty audit |

- Participants: [`workshop/PREPARATION.md`](./workshop/PREPARATION.md) (do at home, ends with `make check`), then [`workshop/exercises/README.md`](./workshop/exercises/README.md)
- Slides: [`facilitator/slides/index.html`](./facilitator/slides/index.html) (offline) and [`facilitator/slides/deck.pdf`](./facilitator/slides/deck.pdf), including the opening video of an autonomous rebuild
- Facilitators: [`facilitator/FACILITATOR.md`](./facilitator/FACILITATOR.md) — timing, reference solutions, troubleshooting

All exercises run locally (Python + `agy`); every exercise has a checkpoint to jump in. Going further — the full five-phase cycle and milestones 2–4 up to Google Cloud Run — is described in [`workshop/README.md`](./workshop/README.md).

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

- **[`/workshop`](./workshop/)**: 90-minute hands-on workshop (EquiGuard) with exercises, checkpoints, slides and the full five-phase cycle for self-study.
- **[`/facilitator`](./facilitator/)**: Facilitator guide, reference solutions and the planted defects — kept outside `workshop/` so coding agents do not read them.
- **[`/slides`](./slides/)**: Offline **Reveal.js deck for the talk** ([`slides/index.html`](./slides/index.html)) plus companion Markdown slide cards (`01`–`19`).
- **[`/governance`](./governance/)**: ADR + LIM templates and framework documentation.
- **[`submission_data.md`](./submission_data.md)**: Rethought title options, elevator pitch, abstracts (EN/DE), key takeaways, and workshop outline.
