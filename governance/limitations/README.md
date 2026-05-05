# Limitation Records

A **Limitation Record (LIM)** documents an *accepted, bounded
weakness* of a system — a place where the project has consciously
decided to live with less than the [BDD Guidelines](../../BDD_GUIDELINES_v1.8.0_EN.md)
or the [ADRs](../adr/) would otherwise demand.

This directory is **not** a general-purpose debt log. It is a
narrow, high-friction mechanism with explicit governance.

## Why bother — the AI-driven angle

Every project accumulates "we know this isn't perfect, but…".
In a hand-driven workflow, those notes live in tribal knowledge,
TODO comments, and stale issues. In an **AI-driven** workflow,
they need to live somewhere the agent can read and respect:

- Without a LIM register, an agent asked to "make the size
  limit configurable" will happily invent a fix that violates
  a deferred-by-design decision.
- With a LIM register, the agent can be prompted to *check
  for a relevant LIM first* and refuse to invent a fix that
  contradicts the documented deferral.

The register is also the place where humans push back on the
AI's tendency to over-engineer. When the agent suggests a
mitigation that the team has already decided not to build,
the LIM is the artifact that says "we know — we chose not to".

## Default posture

> **Every problem is solved cleanly per the BDD Guidelines and
> the ADRs. A Limitation Record is the documented exception,
> never the norm.**

If an implementer (human or AI agent) finds that a clean
solution is "hard", "expensive", or "tedious", that is *not*
cause for a Limitation Record. It is cause to solve the problem.
A Limitation Record applies only when there is a demonstrable,
substantive reason why the clean path cannot be taken — for
instance:

- A theoretical limit of the testing paradigm (e.g.
  API-contract tests inherently share vocabulary with the API
  under test; BDD for C libraries cannot on its own prove
  memory safety).
- An external dependency that the project cannot control (a
  cloud-provider API behaviour, a vendor-internal contract).
- A scope boundary explicitly ruled out by an ADR.

## Governance

Three rules, all mandatory:

1. **No self-approval.** An implementer — including any LLM
   agent — cannot unilaterally declare a limitation. A new
   record must be **reviewed and explicitly approved** by the
   project owner before it is merged. The approval is recorded
   in the "Approved by" field.
2. **No silent acceptance.** A limitation that is not in this
   directory does not exist. Code comments, commit messages,
   or off-band remarks do not substitute for a Limitation
   Record. Shortcuts that are not written down here are bugs,
   not limitations.
3. **Every field is filled.** The [`TEMPLATE.md`](TEMPLATE.md)
   below is the minimum content. "TBD", "N/A", or empty fields
   in a live record are a process violation and block merge.

A pull request that introduces a Limitation Record is held to a
*higher* bar than a pull request that solves the underlying
problem. That asymmetry is intentional — it makes clean
solutions the cheaper path.

## What a record must demonstrate

A convincing record answers, in order:

1. **What is the weakness, precisely?** Vague descriptions hide
   limitations inside other limitations.
2. **Why is the clean solution not chosen?** Cost/benefit,
   theoretical constraint, out-of-scope decision, external
   dependency. Hand-waving ("because BDD can't do it") is
   insufficient.
3. **What mitigations are already in place?** Structural
   cross-checks, redundancy, audits, complementary unit tests,
   sanitizer runs, fuzzing. Absence of mitigations is a red
   flag for the reviewer.
4. **What residual risk remains?** In concrete terms. "Minor
   inconvenience" is not a residual-risk statement; "a heap
   use-after-free in the token cache under contention could
   silently leak a bearer token into an adjacent tenant's
   request, and the BDD suite would not catch it" is.
5. **When must this be revisited?** A trigger condition that
   is observable from the outside. Without a trigger, a
   limitation is forever.

## Lifecycle

```
Proposed -> Accepted -> (Mitigated -> Resolved)
                     -> Superseded by LIM-NNNN
         -> Withdrawn (paydown landed before approval)
```

- **Proposed** — drafted, not yet approved. Must not be merged
  to `main` for binding effect — but if a draft *is* merged
  for review purposes (e.g. to let the owner read it
  in-place), it stays at Proposed until either Accepted or
  Withdrawn.
- **Accepted** — approved by the project owner; known
  limitation in force. Accepted records carry a mandatory
  `Resolution intent` (see below).
- **Mitigated** — further mitigations have been added that
  materially reduce the residual risk. Record remains live.
- **Resolved** — the underlying problem has been solved.
  Record is kept for the history but no longer governs
  anything. The Resolved file MUST carry a `Date resolved:`
  field and a `## Resolution note` section that names the
  paydown commit SHA(s).
- **Withdrawn** — the underlying problem was resolved while
  the record was still at Proposed (the paydown landed during
  review, before the owner ever Accepted the LIM as a debt).
  The record is kept as a brief `Withdrawn` marker — metadata
  block plus a one-paragraph `## Withdrawal note` naming the
  paydown commit SHA. Distinct from Resolved because the
  record never carried the weight of an Accepted debt.
- **Superseded** — replaced by a later record that re-scopes
  the limitation. Both remain in the repository.

Both Resolved and Withdrawn preserve the historical record:
the file remains, the README index lists it, and a future
reader has a direct link to the paydown commit. *Deleting* a
LIM file is non-conformant with the lifecycle.

### Resolution intent

Every `Accepted` record declares itself as one of:

- **`must-resolve`** — a technical debt. Accepted *now*
  because the clean solution cannot yet be built, but a
  paydown is owed. A corresponding task is expected to exist
  in the project tracker, and the record references concrete
  triggers under which the debt becomes due.
- **`permanent`** — an architectural or theoretical boundary.
  No paydown is owed. Triggers for revisit exist for
  completeness (so that future external changes can force
  re-examination) but no active resolution work is expected.

A `must-resolve` record is **not** a softer version of
`permanent`. It is a commitment: the project owes the
underlying problem a clean solution, and the record is the
IOU. Conversion from `must-resolve` to `permanent` requires a
new approval cycle and a superseding record.

## Commit-message conventions

The lifecycle transitions above each have a canonical
commit-verb form. Following these makes the register's
evolution trivially greppable
(`git log --oneline | grep "pay down LIM"`,
`git log --oneline | grep "withdraw LIM"`) and gives
reviewers the right reading frame from the subject line alone:

| Transition                      | Commit verb                                        |
|---------------------------------|----------------------------------------------------|
| File a new LIM (Proposed)       | `docs(scope): record LIM-NNNN — short title`       |
| Proposed → Accepted             | `docs(scope): accept LIM-NNNN [— short reason]`    |
| Accepted → Resolved             | `refactor(scope): resolve LIM-NNNN [via X]`        |
| Proposed → Withdrawn            | `refactor(scope): withdraw LIM-NNNN [— paid down via X]` |
| Accepted → Mitigated            | `docs(scope): note mitigation on LIM-NNNN [via X]` |
| Accepted → Superseded           | `docs(scope): supersede LIM-NNNN by LIM-MMMM`      |

`scope` is the affected component (e.g. the project name, or
`limitations` for register-meta changes). The square-bracketed
suffix is recommended but optional — a one-clause hint at
*what* paydown landed.

Paydown commits (`refactor(scope): resolve…` or
`refactor(scope): withdraw…`) MUST list the touched code
paths in the body, even when the diff is small. A future
reader who finds a stale-looking piece of code via blame
should land on a commit message that explains why it exists,
not just on the diff.

## Numbering & naming

- `NNNN-short-kebab-case-title.md`, numbered sequentially
  starting at `0001`. Numbers are never reused.
- `0000` is reserved for this meta-document.

## Format

Every record uses [`TEMPLATE.md`](TEMPLATE.md). No deviations.

## Index

The example record below illustrates the discipline in the
domain of the [EquiGuard workshop](../../workshop/) — a
GPS-based geofencing system. Adapt it to your own project.

| #    | Title | Status | Intent | Approved by |
|------|-------|--------|--------|-------------|
| 0001 | [V1 supports a single static polygon per pasture](0001-example-single-static-polygon.md) | Accepted | must-resolve | EquiGuard team (2026-04-20) |

## Relationship to ADRs

[ADRs](../adr/) record *decisions that shape the system*.
Limitation Records document *accepted weaknesses in the chosen
direction*. They are not interchangeable:

- An ADR can introduce a new capability.
- A Limitation Record cannot. It only admits a gap.

A Limitation Record typically references one or more ADRs (the
decisions whose clean implementation is being bounded) and,
where relevant, specific sections of the BDD Guidelines.
