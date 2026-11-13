# GCP project ID — single source of truth is the project_id row in
# bdd/mi4_cloud_run.feature. Change it there; the Makefile reads it
# automatically. Local targets (test-mi1, test-mi2, test-mi3) never
# evaluate PROJECT and are not affected.
PROJECT    := $(shell awk -F'|' '/\| *project_id *\|/{gsub(/ /,"",$$3); print $$3; exit}' \
                bdd/mi4_cloud_run.feature 2>/dev/null)

REGISTRY   := europe-west3-docker.pkg.dev
REPO       := equiguard
IMAGE_NAME := geofence-processor
IMAGE_TAG  := v1
LOCAL_TAG  := equiguard/geofence-processor:test
REMOTE_TAG := $(REGISTRY)/$(PROJECT)/$(REPO)/$(IMAGE_NAME):$(IMAGE_TAG)

# Convenience variable for the -var flags passed to every terraform call.
TF_VARS    := -var "project_id=$(PROJECT)" -var "processor_image=$(REMOTE_TAG)"

# Go is only needed for the reference implementation of milestones 2-4.
GO := $(shell command -v go 2>/dev/null || find /usr/local /opt/homebrew/bin -name go -type f 2>/dev/null | head -1)

EMULATOR_FIRESTORE_DIR  := /tmp/equiguard-emulators
EMULATOR_FIRESTORE_PID  := $(EMULATOR_FIRESTORE_DIR)/firestore.pid

WORKSHOP_MODEL := gemini-3.8-flash-high
CHECKPOINT     := .venv/bin/python3 scripts/checkpoint.py

.PHONY: help setup setup-python check build build-mi1 build-image \
        start-emulators stop-emulators \
        test-mi1 test-mi2 test-mi3 test-mi4 test-all \
        workshop-start ex1-start ex1-solution ex2-start ex2-solution \
        ex3-start ex3-solution ex4-start ex4-solution bonus-start bonus-solution \
        phase1-start checkpoint-adrs checkpoint-features checkpoint-steps burn restore-all \
        auth-registry push-image tf-init tf-apply teardown-mi4 clean

# ---------------------------------------------------------------------------
# Default
# ---------------------------------------------------------------------------

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Before the workshop:"
	@echo "  setup                Create the Python test environment (.venv) and the baseline MI1 executable"
	@echo "  check                Self-test: tools, Antigravity CLI login, model, and a green MI1 run"
	@echo ""
	@echo "90-minute workshop (see exercises/README.md):"
	@echo "  workshop-start       Reset to the workshop starting point (your current state is backed up)"
	@echo "  exN-start            Jump to the start of exercise N (1-4); exN-solution loads its reference solution"
	@echo "  bonus-start          Bonus: install a dishonest step file for the step honesty audit"
	@echo "  bonus-solution       Bonus: restore the honest step file"
	@echo "  test-mi1             Milestone 1: geofence library CLI (no infrastructure needed)"
	@echo ""
	@echo "Going further — full five-phase cycle (see README.md):"
	@echo "  phase1-start         Blank slate for Phase 1 (architecture dialogue)"
	@echo "  checkpoint-adrs      Reference ADRs & LIMs (ready for Phase 2)"
	@echo "  checkpoint-features  Reference ADRs, LIMs & feature files (ready for Phases 3/4)"
	@echo "  burn                 Keep spec + steps, delete all application code (ready for Phase 5)"
	@echo "  restore-all          Restore the complete reference workspace including the Go implementation"
	@echo ""
	@echo "Milestones 2-4 (reference implementation in Go):"
	@echo "  build                Build ./bin/geofence-lib-test and ./bin/geofence-processor"
	@echo "  build-image          Build the geofence-processor OCI image ($(LOCAL_TAG))"
	@echo "  start-emulators      Start the Firestore emulator (needs Node.js and Java)"
	@echo "  stop-emulators       Stop the Firestore emulator"
	@echo "  test-mi2             Milestone 2: processor service against the Firestore emulator"
	@echo "  test-mi3             Milestone 3: OCI container image (emulator + Docker)"
	@echo "  test-all             Run MI1 + MI2 + MI3"
	@echo ""
	@echo "Cloud targets (MI4 — real GCP, incurs costs; project ID from bdd/mi4_cloud_run.feature):"
	@echo "  tf-apply             Provision all GCP resources via Terraform"
	@echo "  test-mi4             Run MI4 BDD tests against live Cloud Run"
	@echo "  teardown-mi4         Destroy all GCP resources (stops billing)"
	@echo "  clean                Remove compiled binaries"

# ---------------------------------------------------------------------------
# Setup & self-test
# ---------------------------------------------------------------------------

setup-python:
	@if [ ! -x .venv/bin/behave ] || ! .venv/bin/python3 -m pip --version >/dev/null 2>&1; then \
		echo "Setting up Python virtual environment (.venv)..."; \
		rm -rf .venv; \
		python3 -m venv .venv; \
		.venv/bin/pip install -q -r requirements.txt; \
	fi

setup: setup-python
	@mkdir -p bin
	@if [ ! -e bin/geofence-lib-test ] && [ ! -f build.sh ] && [ ! -f .burned ]; then \
		$(CHECKPOINT) install-baseline; \
	fi

check: setup
	@.venv/bin/python3 scripts/check.py --model $(WORKSHOP_MODEL)

# ---------------------------------------------------------------------------
# Build (language-neutral, ADR-0004)
# ---------------------------------------------------------------------------

# Milestone 1 needs only ./bin/geofence-lib-test. A ./build.sh (written by the
# agent in any language) takes precedence; otherwise the existing executable is used.
build-mi1:
	@mkdir -p bin
	@if [ -f ./build.sh ]; then \
		echo "Running ./build.sh..."; \
		bash ./build.sh || exit 1; \
		chmod +x bin/geofence-lib-test 2>/dev/null || true; \
	elif [ -e bin/geofence-lib-test ]; then \
		chmod +x bin/geofence-lib-test; \
	else \
		echo "No ./bin/geofence-lib-test yet (RED specification mode)."; \
	fi

build: setup-python build-mi1
	@if [ -f ./build.sh ]; then \
		chmod +x bin/geofence-processor 2>/dev/null || true; \
	elif [ -f go.mod ] && [ -n "$(GO)" ]; then \
		echo "Building the Go reference implementation into bin/..."; \
		$(GO) build -o bin/geofence-processor ./cmd/geofence-processor/; \
		[ -e bin/geofence-lib-test ] || $(GO) build -o bin/geofence-lib-test ./cmd/geofence-lib-test/; \
	elif [ -f go.mod ]; then \
		echo "Go toolchain not found: skipping ./bin/geofence-processor (only needed for MI2-MI4)."; \
	fi

build-image:
	@if [ -f Dockerfile ]; then \
		echo "Building Docker image $(LOCAL_TAG)..."; \
		docker build -t $(LOCAL_TAG) .; \
	else \
		echo "No Dockerfile found yet (RED specification mode)."; \
	fi

# ---------------------------------------------------------------------------
# 90-minute workshop checkpoints (scripts/checkpoint.py backs up your files
# to .workshop-backup/ before it overwrites anything)
# ---------------------------------------------------------------------------

workshop-start: setup-python
	@$(CHECKPOINT) workshop-start

ex1-start ex1-solution ex2-start ex2-solution ex3-start ex3-solution ex4-start ex4-solution bonus-start bonus-solution: setup-python
	@$(CHECKPOINT) $@

# ---------------------------------------------------------------------------
# Full five-phase cycle checkpoints (Going further)
# ---------------------------------------------------------------------------

BURN_PATHS := cmd/ internal/ go.mod go.sum Dockerfile bin/ src/ app/ lib/ \
              package.json package-lock.json tsconfig.json node_modules/ dist/ \
              Cargo.toml Cargo.lock target/ pyproject.toml build.sh

phase1-start: clean
	@echo "Resetting workspace for Phase 1 (Architecture Dialogue)..."
	rm -rf $(BURN_PATHS)
	rm -f governance/adr/000[1-9]*.md governance/limitations/000*.md
	rm -f bdd/00_error_path_enumeration.md bdd/mi*.feature
	rm -f bdd/steps/geofence_steps.py bdd/steps/processor_steps.py bdd/steps/image_steps.py bdd/steps/cloud_steps.py
	@echo "Ready for Phase 1. Start Antigravity CLI with prompts/01-architecture-dialogue.md"

checkpoint-adrs:
	@echo "Restoring reference ADRs and LIMs (Phase 1 complete -> ready for Phase 2)..."
	git checkout HEAD -- governance/
	@echo "Reference ADRs (0000-0004) and LIMs (0001-0002) restored in governance/."

checkpoint-features: checkpoint-adrs
	@echo "Restoring reference error path enumeration and feature files (ready for Phases 3/4)..."
	git checkout HEAD -- bdd/00_error_path_enumeration.md bdd/mi1_geofence_library.feature bdd/mi2_geofence_processor.feature bdd/mi3_geofence_processor_image.feature bdd/mi4_cloud_run.feature
	@echo "Reference feature files restored in bdd/."

checkpoint-steps: checkpoint-features
	@echo "Restoring reference step definitions and burning application code (ready for Phase 5)..."
	git checkout HEAD -- bdd/steps/ bdd/environment.py
	rm -rf $(BURN_PATHS)
	touch .burned
	@echo "Specification and steps ready (RED). Application code removed."
	@echo "Run 'make test-mi1' to verify the RED state, then use prompts/05-autonomous-implementation.md."

burn: checkpoint-steps

restore-all:
	@echo "Restoring complete reference workspace (spec + steps + Go implementation)..."
	rm -rf $(BURN_PATHS) .burned
	git checkout HEAD -- governance/ bdd/ cmd/ internal/ go.mod go.sum Dockerfile Makefile
	@echo "Workspace restored."

# ---------------------------------------------------------------------------
# Emulator lifecycle (MI2, MI3): Firestore via npx firebase-tools (Node.js + Java)
# Pub/Sub push deliveries are simulated as HTTP POSTs by the steps (ADR-0004),
# so no Pub/Sub emulator is required.
# ---------------------------------------------------------------------------

start-emulators:
	@java_major=$$(java -version 2>&1 | awk -F'"' '/version/{split($$2,v,"."); print v[1]; exit}'); \
	 if [ -z "$$java_major" ] || [ "$$java_major" -lt 21 ]; then \
		echo "ERROR: the Firestore emulator (firebase-tools 15) needs Java 21 or newer (found: $${java_major:-none})."; \
		exit 1; \
	 fi
	@echo "Starting Firestore emulator..."
	@mkdir -p $(EMULATOR_FIRESTORE_DIR)
	@printf '{"emulators":{"firestore":{"port":8082,"host":"localhost"},"ui":{"enabled":false}}}' \
		> $(EMULATOR_FIRESTORE_DIR)/firebase.json
	@cd $(EMULATOR_FIRESTORE_DIR) && \
		nohup npx --yes firebase-tools@15.11.0 emulators:start \
			--only firestore --project equiguard-test \
			> $(EMULATOR_FIRESTORE_DIR)/firestore.log 2>&1 & \
		echo $$! > $(EMULATOR_FIRESTORE_PID)
	@echo "Waiting for Firestore emulator on :8082 (first start downloads the emulator)..."
	@for i in $$(seq 180); do \
		curl -sf http://localhost:8082 >/dev/null 2>&1 && { echo "Emulator ready."; exit 0; }; \
		kill -0 $$(cat $(EMULATOR_FIRESTORE_PID)) 2>/dev/null || break; \
		sleep 1; \
	 done; \
	 echo "ERROR: Firestore emulator did not start. Last lines of $(EMULATOR_FIRESTORE_DIR)/firestore.log:"; \
	 tail -n 15 $(EMULATOR_FIRESTORE_DIR)/firestore.log; exit 1

stop-emulators:
	@if [ -f $(EMULATOR_FIRESTORE_PID) ]; then \
		kill $$(cat $(EMULATOR_FIRESTORE_PID)) 2>/dev/null || true; \
		rm -f $(EMULATOR_FIRESTORE_PID); \
	fi
	@pkill -f "[c]loud-firestore-emulator" 2>/dev/null || true
	@echo "Emulator stopped."

# ---------------------------------------------------------------------------
# Local BDD tests (MI1 – MI3)
# ---------------------------------------------------------------------------

test-mi1: setup-python build-mi1
	@echo "=== Milestone 1: Geofence Library ==="
	@.venv/bin/behave bdd/ --tags=@mi1

test-mi2: build start-emulators
	@echo "=== Milestone 2: Geofence Processor (Firestore emulator) ==="
	@.venv/bin/behave bdd/ --tags=@mi2; \
	 status=$$?; $(MAKE) --no-print-directory stop-emulators; exit $$status

test-mi3: build build-image start-emulators
	@echo "=== Milestone 3: OCI Image ==="
	@.venv/bin/behave bdd/ --tags=@mi3; \
	 status=$$?; $(MAKE) --no-print-directory stop-emulators; exit $$status

test-all: build build-image start-emulators
	@echo "=== Running MI1 + MI2 + MI3 ==="
	@.venv/bin/behave bdd/ --tags='@mi1 or @mi2 or @mi3'; \
	 status=$$?; $(MAKE) --no-print-directory stop-emulators; exit $$status

# ---------------------------------------------------------------------------
# Cloud — image push
# ---------------------------------------------------------------------------

auth-registry:
	@echo "Configuring Docker authentication for Artifact Registry..."
	gcloud auth configure-docker $(REGISTRY) --quiet

push-image: build build-image auth-registry
	@echo "Tagging $(LOCAL_TAG) → $(REMOTE_TAG)"
	docker tag $(LOCAL_TAG) $(REMOTE_TAG)
	@echo "Pushing $(REMOTE_TAG)..."
	docker push $(REMOTE_TAG)

# ---------------------------------------------------------------------------
# Cloud — Terraform
# ---------------------------------------------------------------------------

tf-init:
	@echo "Initializing Terraform..."
	terraform -chdir=terraform init -input=false

tf-apply: tf-init
	@echo "Phase 1: provisioning Artifact Registry..."
	terraform -chdir=terraform apply -auto-approve -input=false \
		-target=google_artifact_registry_repository.equiguard \
		$(TF_VARS)
	@echo "Pushing image to registry..."
	$(MAKE) --no-print-directory push-image
	@echo "Phase 2: provisioning Cloud Run, Pub/Sub, and subscription..."
	terraform -chdir=terraform apply -auto-approve -input=false \
		$(TF_VARS)

# ---------------------------------------------------------------------------
# Cloud — MI4 BDD tests
# ---------------------------------------------------------------------------

test-mi4: setup-python
	@echo "=== Milestone 4: Cloud Run (LIVE GCP — project: $(PROJECT)) ==="
	@echo "Checking prerequisites..."
	@terraform -chdir=terraform output cloud_run_url >/dev/null 2>&1 || { \
		echo ""; \
		echo "ERROR: Terraform outputs not found."; \
		echo "       Run 'make tf-apply' before 'make test-mi4'."; \
		echo ""; \
		exit 1; \
	}
	@gcloud auth print-identity-token >/dev/null 2>&1 || { \
		echo ""; \
		echo "ERROR: No active gcloud credentials."; \
		echo "       Run: gcloud auth application-default login"; \
		echo ""; \
		exit 1; \
	}
	@echo "Prerequisites OK."
	@echo "WARNING: This test uses real GCP resources and incurs costs."
	@.venv/bin/behave bdd/ --tags=@mi4 -D project_id=$(PROJECT)

# ---------------------------------------------------------------------------
# Teardown
# ---------------------------------------------------------------------------

teardown-mi4:
	@echo "Destroying all GCP resources for project $(PROJECT)..."
	@echo "This will delete: Cloud Run, Pub/Sub, Artifact Registry repository."
	@read -p "Are you sure? [y/N] " confirm && [ "$$confirm" = "y" ]
	terraform -chdir=terraform destroy -auto-approve -input=false \
		$(TF_VARS)
	@echo "Teardown complete."

# ---------------------------------------------------------------------------
# Clean
# ---------------------------------------------------------------------------

clean:
	@rm -rf bin/
	@echo "Cleaned."
