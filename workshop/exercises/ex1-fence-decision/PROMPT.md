We are in the EquiGuard workshop repository. Read AGENTS.md, governance/adr/0001-point-in-polygon-ray-casting.md, governance/adr/TEMPLATE.md, governance/limitations/TEMPLATE.md and the two README index files in governance/adr/ and governance/limitations/.

ADR-0001 decides that we use even-odd ray casting. It does not decide what happens when a GPS point lies exactly on the fence, that is, on an edge or on a vertex of the pasture polygon. Ray casting is ambiguous there.

Conduct a short architecture dialogue with me about this gap, strictly following section 2 of AGENTS.md: ask exactly ONE question per message, each with context, options, your recommendation with a one-sentence reason, and the consequences. Wait for my answer before the next question. Cover these three questions:
1. Does a point on the fence count as inside or outside the pasture?
2. Which numerical tolerance decides that a point is "on the fence" (floating-point rounding only, stated in degrees)?
3. Do we model GPS accuracy (a tolerance band in metres) in V1, or do we defer it?

After my third answer:
- Write governance/adr/0005-<short-slug>.md (ADR-0005) from the template, including the mandatory sections Security Implications and Alternatives Considered.
- If we deferred something, write governance/limitations/0004-<short-slug>.md (LIM-0004) from the template.
- Add the new records to both README index tables.
- Do not change feature files, step definitions or any code.
