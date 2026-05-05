# Governance: ADR + LIM + BDD as a triad

This directory documents the **decision-and-debt governance**
that complements the [BDD Guidelines](../BDD_GUIDELINES_v1.8.0_EN.md).

The Guidelines answer the question *"how do we write executable
specifications that are tight enough to drive both humans and AI
agents?"*. They do not answer two adjacent questions that every
real project hits:

1. *"How do we record the architectural decisions that shape the
   system around the spec?"*
2. *"How do we admit, in a disciplined way, the cases where the
   spec or an architectural decision cannot be honoured cleanly
   right now?"*

This `governance/` directory addresses both, with two small
repositories of records that sit alongside the Guidelines:

- [`adr/`](adr/) — **Architecture Decision Records**, in the
  Nygard tradition with two mandatory sections added (Security
  Implications, Alternatives Considered).
- [`limitations/`](limitations/) — **Limitation Records (LIMs)**,
  a high-friction register for accepted, bounded weaknesses.

Together, the three artifacts form a triad:

```
            BDD Guidelines (this repo's headline)
                         │
                         │  drives implementation,
                         │  defines the contract
                         ▼
                  ┌──────────────┐
                  │  .feature    │  the spec
                  │  files       │  (what the system does)
                  └──────────────┘
                         │
            ┌────────────┴────────────┐
            ▼                         ▼
    ┌──────────────┐           ┌──────────────┐
    │     ADRs     │           │     LIMs     │
    │ (decisions   │           │ (accepted    │
    │  *behind*    │           │  weaknesses  │
    │  the spec)   │           │  *against*   │
    │              │           │  the spec or │
    │              │           │  ADRs)       │
    └──────────────┘           └──────────────┘
```

Each axis has its own discipline:

| Axis              | Asks                                  | Answers via            |
|-------------------|---------------------------------------|------------------------|
| BDD .feature      | *What does the system do?*            | Gherkin scenarios      |
| ADRs              | *Why is it built this way?*           | Decision records       |
| LIMs              | *Where do we knowingly fall short?*   | Limitation records     |

The three are mutually referential. An ADR may cite a Guidelines
section that motivates it. A LIM names the ADR or Guidelines
section it bounds. A BDD scenario can land a `# LIM-NNNN` comment
above an explicitly skipped or under-asserted step.

## Why bother — the AI-driven angle

The Guidelines argue that BDD's strict structure is now a feature
for AI orchestration: an agent that has the .feature file in
context produces tighter, more reproducible code than one that
free-styles from a chat prompt. ADRs and LIMs extend that
argument:

- An agent that reads the relevant ADRs **stops re-litigating
  decisions in every prompt**. "Use a single GCP project" is a
  one-line ADR-0009 reference instead of a recurring debate.
- A LIM register **tells the agent what *not* to fix**. An agent
  asked to "make the size limit configurable" should find LIM
  0019 first and refuse to invent a fix that contradicts the
  documented deferral.
- The `Withdrawn` lifecycle state on LIMs (see
  [`limitations/README.md`](limitations/README.md)) lets a paydown
  land *during* the review window without the LIM accumulating
  weight as an accepted debt — a small but recurring AI-workflow
  pattern: the agent flags a debt, the human reviews, and either
  the debt sticks or the paydown lands within minutes.

## How to adopt

Pick the smallest scope that makes the discipline pay back. A
solo project rarely needs both registers; a multi-component
codebase that an AI agent navigates probably needs both.

1. **Start with one ADR.** The first decision an ADR makes in a
   new project is usually [`adr/0000-record-architecture-decisions.md`](adr/TEMPLATE.md)
   — the meta-decision *"we use ADRs"*. Everything else follows.
2. **Add the LIM register the first time you defer something.**
   A V1 that ships without a feature, an algorithm with a known
   suboptimal worst case, a test that asserts on observable
   behaviour rather than invariant: each is the first LIM.
3. **Wire the conventions into commit messages.** The
   [LIM commit-verb table](limitations/README.md#commit-message-conventions)
   makes the register's evolution greppable from `git log` alone.
4. **Make the agent read them.** When prompting an agent for a
   non-trivial change, include the relevant ADR + any LIM that
   bounds it. The agent's output quality jumps measurably.

## What's in this directory

- [`README.md`](README.md) — this file (the framework overview).
- [`adr/`](adr/) — Architecture Decision Records:
  - [`README.md`](adr/README.md) — ADR governance.
  - [`TEMPLATE.md`](adr/TEMPLATE.md) — per-record skeleton.
  - [`0001-example-…`](adr/) — a worked example using the
    EquiGuard workshop as the domain.
- [`limitations/`](limitations/) — Limitation Records:
  - [`README.md`](limitations/README.md) — LIM governance,
    including the four-state lifecycle (Proposed → Accepted /
    Withdrawn / Resolved / Superseded) and commit-message
    conventions.
  - [`TEMPLATE.md`](limitations/TEMPLATE.md) — per-record
    skeleton.
  - [`0001-example-…`](limitations/) — a worked example using the
    EquiGuard workshop as the domain.

The records under `adr/0001-…` and `limitations/0001-…` are
illustrative templates only — copy and adapt them in your own
project. The discipline lives in the README files; the example
records show what the discipline looks like in practice.
