Read AGENTS.md (section 3.3), BDD_GUIDELINES_v1.9.0_EN.md (sections 2.1, 4.2 and 4.5), governance/adr/0005-*.md, governance/limitations/0004-*.md if it exists, bdd/00_error_path_enumeration.md and bdd/mi1_geofence_library.feature.

Turn ADR-0005 (points on the fence) into an executable specification, in this order:

1. Error paths first: add the boundary cases to Layer 1 of bdd/00_error_path_enumeration.md as new rows (point exactly on a vertex, point exactly on an edge, points within and beyond the numerical tolerance of ADR-0005, points just beyond and just inside the fence as negative controls, and anything ADR-0005 or LIM-0004 deliberately defers, marked `none` with its reason). Update the summary table.

2. Then add ONE new Scenario Outline to bdd/mi1_geofence_library.feature, tagged `@mi1 @boundary`, that uses the existing HomePasture polygon from the Background and the existing steps:
   - every vertex of HomePasture,
   - the midpoint of every HomePasture edge (computed exactly from the two vertices; up to 8 decimal places are fine),
   - tolerance checks: a point half the ADR-0005 tolerance and a point twice the ADR-0005 tolerance beyond the fence, once east of the midpoint of the east edge and once south of the second vertex (the south-eastern corner),
   - negative controls 1e-6 degrees beyond and 1e-6 degrees inside the east edge and the south edge,
   - the expected `is_inside` for each row taken from ADR-0005, and a `point_id` column that names each case.
   Extend the `# Source:` header with ADR-0005 (and LIM-0004 if it exists).

3. Do NOT change existing scenarios, step definitions or any application code. Every value must be visible in the Gherkin text.

4. Run `make test-mi1`. The new scenarios must fail (RED) because the current implementation knows nothing about the fence; the 16 existing scenarios must still pass. Report which rows fail and why, in at most five lines.

5. Follow AGENTS.md section 4: do not use reference solutions, checkpoints or git history.
