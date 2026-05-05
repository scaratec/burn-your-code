# Architecture Decision Records

This directory holds the **Architecture Decision Records (ADRs)**
for a project: one record per architectural decision, immutable
once accepted, superseded but never edited.

The format is [Michael Nygard's original proposal][nygard],
extended with two mandatory sections (Security Implications,
Alternatives Considered) that experience has shown are the two
most-skipped and most-asked-for sections in retrospect.

[nygard]: https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions

## Why this discipline

ADRs answer the question *"why is this system built the way it
is?"* — once, in writing, at the moment the decision is made.
The alternative is "tribal knowledge": the rationale lives in
the original author's head, leaks slowly through Slack
fragments, and is inaccessible to a new hire (human or AI agent)
six months later.

In the AI-driven workflow this repository documents, ADRs serve
a second purpose: **they are context for the agent**. An agent
prompted with the relevant ADRs in its context window does not
re-litigate decisions already made. "Use a single GCP project
for all tenant resources" is a one-line ADR-0009 reference, not
a recurring debate.

## Format

All ADRs follow [`TEMPLATE.md`](TEMPLATE.md). The mandatory
sections are:

- **Context** — the forces at play and why a decision is needed
  *now*. Factual; no decision yet.
- **Decision** — what was decided, in one unambiguous sentence,
  followed by the mechanism.
- **Consequences** — positive, negative, and neutral. Honest;
  the reader should be able to tell from this section alone
  whether the decision is a good fit for their situation.
- **Security Implications** — required for every ADR. Attack
  surface, trust boundaries, data exposure, failure modes,
  auditability. If an ADR has no security implications, it
  states that explicitly and argues why.
- **Alternatives Considered** — required for every ADR. Each
  rejected option with a one-line description and the reason
  for rejection. Prevents future re-litigation.
- **References** — RFCs, prior art, related ADRs, discussion
  threads.

The two mandatory extensions exist because the most common
"why didn't anyone think of X?" questions six months later
are *security* questions and *alternatives* questions.

## Numbering & naming

- ADRs are numbered sequentially, zero-padded to four digits:
  `0001`, `0002`, …
- File name: `NNNN-short-kebab-case-title.md`
- `0000` is reserved for the meta-ADR that establishes the ADR
  process itself ("we use ADRs").
- Numbers are never reused. A deprecated or superseded ADR
  keeps its number.

## Lifecycle

```
Proposed  →  Accepted  →  (Deprecated | Superseded by ADR-XXXX)
```

- **Proposed** — authored, under discussion, not yet binding.
  Lives in the same directory; its Status field declares the
  pending state. A Proposed ADR may be merged to `main` for
  in-place review (a draft that has not been Accepted is still
  authoritative-as-draft, not a hidden side document).
- **Accepted** — the decision is in force. Binding until
  deprecated or superseded.
- **Deprecated** — the decision no longer applies, but no
  replacement is in force. The system has either dropped the
  capability the ADR governed, or moved to a regime where the
  decision is no longer meaningful.
- **Superseded** — replaced by a named later ADR. Both remain
  in the repository; the superseded ADR's Status line names
  the replacement.

Status transitions are themselves recorded: when an ADR moves
to Superseded, edit its Status line and link the replacement.
**Do not delete the file.**

## Writing rules

1. **One decision per ADR.** If you are tempted to describe
   two, write two. Bundling decisions makes future
   supersession harder than it needs to be.
2. **Present tense, active voice.** "We use X" not "X will be
   used".
3. **Stand on its own.** A reader should not need prior ADRs
   to understand this one — link explicitly to anything
   required.
4. **Keep it short.** Under 500 lines. If it grows larger,
   split it or move detail into a linked specification document.
5. **No code.** ADRs describe decisions, not implementations.
   Pseudo-code for illustration is fine; real code belongs in
   the implementation.
6. **Write for a reader who is not in the room.** The original
   author's memory is not a documentation strategy.
7. **Alternatives Considered mirrors the actual discussion.**
   List the options that were truly on the table — not
   constructed strawmen invented after the fact. The reason
   for rejection should be the *actual* reason, not a
   post-hoc rationalization.

## Relationship to LIMs

When an ADR's clean implementation is bounded — V1 ships
without a feature the ADR contemplates, an algorithm has a
known suboptimal worst case, a security control is deferred —
the bound is recorded as a [Limitation Record](../limitations/),
not as a TODO comment in the ADR. The LIM cites the ADR it
bounds; the ADR can optionally cite the LIM in its References
section once the LIM is Accepted.

The two registers are intentionally separate: ADRs are about
*what we do*; LIMs are about *what we knowingly fail to do*.

## Index

The example records below illustrate the discipline in the
domain of the [EquiGuard workshop](../../workshop/) — a
GPS-based geofencing system. Adapt them to your own project.

| #    | Title                                            | Status   |
|------|--------------------------------------------------|----------|
| 0001 | [Point-in-polygon: ray casting over winding number](0001-example-point-in-polygon-ray-casting.md) | Accepted |
