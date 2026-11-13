# ADR 0000: Record architecture decisions, limitations, and BDD specifications as a triad

- **Status:** Accepted
- **Date:** 2026-11-10
- **Deciders:** EquiGuard Architecture Team

## Context

EquiGuard is developed using an AI-native, specification-first workflow where AI agents (Gemini via Antigravity CLI) generate the application code autonomously from the repository's specification. Without recorded architectural decisions and explicit scope boundaries, an AI agent has no memory across sessions: it re-negotiates technology choices in every prompt, invents ad-hoc schemas, or attempts to "fix" deliberate V1 simplifications.

## Decision

We govern EquiGuard through a three-register specification triad, sequenced strictly before application code ([`AGENTS.md` §3](../../AGENTS.md)):

1. **Architecture Decision Records (`governance/adr/`)** — *Why* the system is structured the way it is, using [`TEMPLATE.md`](TEMPLATE.md) with mandatory `Security Implications` and `Alternatives Considered` sections.
2. **Limitation Records (`governance/limitations/`)** — *Where* V1 knowingly accepts a bounded shortcut against an ADR or requirement, using [`../limitations/TEMPLATE.md`](../limitations/TEMPLATE.md).
3. **Executable Gherkin Feature Files (`bdd/*.feature`)** — *What* the system does observably from the outside, following [BDD Guidelines v1.9.0](../../../BDD_GUIDELINES_v1.9.0_EN.md).

Before step code or application code is written, an independent **Specification Critic (`bdd-critic`, Guidelines §14)** audits all three registers together along with [`bdd/00_error_path_enumeration.md`](../../bdd/00_error_path_enumeration.md).

## Consequences

### Positive

- The specification is complete, self-contained, and fits into a single LLM context window so an agent can audit or implement the entire service without human intervention.
- Architectural rationale and deliberate V1 boundaries survive full code rewrites across programming languages.

### Negative

- Upfront effort is required before the first line of application code exists.

### Neutral

- Accepted ADRs are immutable; changing a decision requires a new ADR that supersedes the old one.

## Security Implications

Mandatory `Security Implications` sections in every ADR ensure that trust boundaries, authentication mechanisms, and input validation rules are decided before code generation rather than bolted on afterwards.

## Alternatives Considered

- **Free-form chat prompting ("Vibe Coding").** Rejected because decisions remain trapped in ephemeral chat history, producing unmaintainable code with no regression safety.
- **Gherkin feature files without ADRs or LIMs.** Rejected because feature files state *what* the system does, not *why* alternatives were rejected or *which* omissions are deliberate (LIMs).

## References

- [`AGENTS.md`](../../AGENTS.md)
- [BDD Guidelines v1.9.0](../../../BDD_GUIDELINES_v1.9.0_EN.md)
