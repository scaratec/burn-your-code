# LIM NNNN: <Short Noun Phrase>

- **Status:** Proposed | Accepted | Mitigated | Resolved | Withdrawn | Superseded by [LIM-XXXX](XXXX-title.md)
- **Resolution intent:** must-resolve (technical debt) | permanent (architectural boundary)
- **Date proposed:** YYYY-MM-DD
- **Date approved:** YYYY-MM-DD (required before Accepted; n/a if Withdrawn)
- **Date resolved:** YYYY-MM-DD (required for Resolved)
- **Date withdrawn:** YYYY-MM-DD (required for Withdrawn)
- **Proposed by:** <name or agent id>
- **Approved by:** <project-owner name, required before Accepted; n/a if Withdrawn>
- **Resolution commit:** <git SHA, required for Resolved>
- **Withdrawal commit:** <git SHA, required for Withdrawn>
- **Scope:** <component this limitation applies to>
- **Related ADRs:** [ADR-XXXX](../adr/XXXX-title.md), …
- **Related Guidelines:** BDD Guidelines §N.N, §N.N

## Resolution intent

Mandatory classification for `Accepted` records. Every
limitation is one of two kinds:

- **`must-resolve`** — a technical debt that is accepted *now*
  but must be paid back. The record must list an explicit
  resolution plan (even if the timing is uncertain) and
  concrete paydown triggers in the "Triggers for revisit"
  section. A `must-resolve` record is tracked as an open debt
  item in the project's task list until its status becomes
  `Resolved`.
- **`permanent`** — an architectural or theoretical boundary
  that the project has decided to live with indefinitely. No
  resolution is expected. The record still lists "Triggers
  for revisit" so that future external advances (new tooling,
  new standards, changed threat model) can force a
  re-examination, but no paydown is owed.

"Not sure" is not a valid value. If the classification cannot
be argued convincingly for one of the two, the record is not
ready for approval.

## Context

Where in the system does this limitation arise? Which ADR or
guideline would dictate a different, cleaner outcome, and why
can it not be reached? Describe the terrain factually — the
reviewer must be able to understand the constraint without
prior briefing.

## Nature of the weakness

State the limitation precisely. Not "the BDD suite is not
perfect" — say *exactly* which property is missing, under
*which conditions*, and with *which observable consequence*.
Vague records are rejected at review.

## Why the clean solution is not chosen

Justify the exception. Acceptable reasons include:

- A theoretical limit (BDD contract tests share vocabulary
  with the API under test; BDD for C cannot prove memory
  safety; property-based tests on generated inputs lie
  outside the BDD paradigm; etc.).
- A disproportionate cost vs. the residual risk, with numbers.
- An external dependency outside project control (a
  cloud-provider API contract, a vendor-internal interface).
- An explicit scope boundary from a superseded ADR.

Unacceptable reasons: "it's hard", "we ran out of time", "the
ADR is too strict". Those lead to doing the work, not to a
Limitation Record.

## Mitigations in place

List every mitigation that reduces the residual risk. Each
entry should be concrete enough that a reviewer can verify it
exists:

- Structural cross-check in scenarios (field X consistent
  with Y).
- Separate contract test (`path/to/feature.feature`).
- Sanitizer or fuzzing coverage (AddressSanitizer, UBSan,
  Valgrind, libFuzzer) at `path/to/harness`.
- Spec-audit checklist item.
- Runtime invariant enforced at module X.

Absence of mitigations is a red flag. A record with no
mitigations is effectively "we accept the problem as-is" and
must argue explicitly why no mitigation is possible.

## Residual risk

Describe, in concrete terms, the worst case that can still
happen. A good residual-risk statement reads like a bug
report the author would *expect* to see one day. Vague
phrasings ("minor risk", "limited exposure") are rejected.

## Triggers for revisit

Under which externally observable conditions must this record
be re-examined? Examples:

- If the spec audit produces ≥ N findings attributable to
  this limitation.
- If a new ADR changes the underlying architecture.
- If an external tooling advance removes the theoretical
  barrier.
- If an incident report links to this record.

"Never" is not a trigger. Every limitation must have at
least one.

## References

- ADR links.
- Guideline sections.
- External material (RFCs, papers, tooling documentation).
- Discussion threads or issue tracker entries, if applicable.
