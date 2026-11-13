Implement the EquiGuard geofence library CLI (milestone 1) in LANGUAGE completely from its specification.

The specification is finished and read-only:
- governance/adr/ (especially ADR-0001, ADR-0004 and ADR-0005) and governance/limitations/
- bdd/00_error_path_enumeration.md, bdd/mi1_geofence_library.feature, bdd/steps/ and bdd/environment.py

Provide:
- the source code of the CLI in LANGUAGE, all of it under app/ (create the directory),
- an executable ./build.sh that builds or installs it as ./bin/geofence-lib-test (make test-mi1 runs ./build.sh automatically),
- the contract from ADR-0004: read {"point": {"lon": ..., "lat": ...}, "polygon": [{"lon": ..., "lat": ...}, ...]} as JSON on stdin and write {"is_inside": true|false} as JSON on stdout.

Rules:
- Do not modify anything under governance/ or bdd/. If you believe a scenario is wrong, leave it and report it at the end.
- Ask no questions; every decision is already in the ADRs and the feature file.
- Use only the standard library of LANGUAGE (ADR-0001: no geometry libraries).
- Follow AGENTS.md section 4: do not use reference solutions, checkpoints or git history.

Scope: milestone 1 only. Ignore milestones 2–4 (processor, Dockerfile, make test-all); see AGENTS.md section 4.

You are done only when `make test-mi1` passes twice in a row with 0 failed scenarios. At the end, print the numbers: scenarios passed / failed, and the lines of code you wrote.
