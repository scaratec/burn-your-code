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

# Auto-detect Go binary — works regardless of installation path
GO := $(shell which go 2>/dev/null \
        || find /usr/local /opt/homebrew/bin -name go -type f 2>/dev/null \
           | head -1 \
        || echo go)

EMULATOR_PUBSUB_NAME    := equiguard-pubsub-emulator
EMULATOR_PUBSUB_IMAGE   := gcr.io/google.com/cloudsdktool/cloud-sdk:latest
EMULATOR_FIRESTORE_DIR  := /tmp/equiguard-emulators
EMULATOR_FIRESTORE_PID  := $(EMULATOR_FIRESTORE_DIR)/firestore.pid

.PHONY: help setup setup-python build build-image \
        start-emulators stop-emulators \
        test-mi1 test-mi2 test-mi3 test-mi4 test-all \
        phase1-start checkpoint-adrs checkpoint-features checkpoint-steps burn restore-all \
        auth-registry push-image \
        tf-init tf-apply teardown-mi4 \
        clean

# ---------------------------------------------------------------------------
# Default
# ---------------------------------------------------------------------------

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Workshop Phase & Checkpoint targets:"
	@echo "  phase1-start         Reset to blank template for Phase 1 (ADR dialogue with agy)"
	@echo "  checkpoint-adrs      Restore reference ADRs & LIMs (ready for Phase 2: Features)"
	@echo "  checkpoint-features  Restore reference ADRs, LIMs & Features (ready for Phase 3/4: Critic & Steps)"
	@echo "  burn                 Keep full Spec + Steps, delete all app code (ready for Phase 5: Polyglot Build)"
	@echo "  restore-all          Restore complete reference workspace including Go implementation"
	@echo ""
	@echo "Local Build & BDD targets (Language-Neutral):"
	@echo "  setup                Install Python BDD venv (+ resolve language deps if present)"
	@echo "  build                Build ./bin/geofence-lib-test and ./bin/geofence-processor (any language)"
	@echo "  build-image          Build the geofence-processor OCI image ($(LOCAL_TAG))"
	@echo "  start-emulators      Start Firestore (npx) + Pub/Sub (Docker) emulators"
	@echo "  stop-emulators       Stop and remove emulators"
	@echo "  test-mi1             Milestone 1: Geofence Library CLI (no infra needed)"
	@echo "  test-mi2             Milestone 2: Processor Service (emulators managed automatically)"
	@echo "  test-mi3             Milestone 3: OCI Container Image (emulators + Docker)"
	@echo "  test-all             Run MI1 + MI2 + MI3"
	@echo ""
	@echo "Cloud targets (MI4 — real GCP, incurs costs):"
	@echo "  Project ID is read from bdd/mi4_cloud_run.feature (project_id row)."
	@echo "  auth-registry        Configure Docker for Artifact Registry"
	@echo "  push-image           Tag and push image to Artifact Registry"
	@echo "  tf-init              Initialize Terraform"
	@echo "  tf-apply             Provision all GCP resources via Terraform"
	@echo "  test-mi4             Run MI4 BDD tests against live Cloud Run"
	@echo "  teardown-mi4         Destroy all GCP resources (stops billing)"
	@echo "  clean                Remove compiled binaries"

# ---------------------------------------------------------------------------
# Local setup & polyglot build (ADR-0004)
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
	@if [ -f go.mod ]; then \
		echo "Go module detected ($(GO)) — running go mod tidy..."; \
		$(GO) mod tidy; \
	fi

build: setup
	@mkdir -p bin
	@if [ -f ./build.sh ]; then \
		echo "Running custom ./build.sh..."; \
		bash ./build.sh; \
		chmod +x bin/geofence-lib-test bin/geofence-processor 2>/dev/null || true; \
	elif [ -f go.mod ]; then \
		echo "Building Go binaries into bin/..."; \
		$(GO) build -o bin/geofence-processor ./cmd/geofence-processor/; \
		$(GO) build -o bin/geofence-lib-test  ./cmd/geofence-lib-test/; \
	elif [ -f Cargo.toml ]; then \
		echo "Building Rust binaries into bin/..."; \
		cargo build --release; \
		cp target/release/geofence-processor bin/ 2>/dev/null || true; \
		cp target/release/geofence-lib-test  bin/ 2>/dev/null || true; \
	elif [ -f bin/geofence-lib-test ] || [ -f bin/geofence-processor ]; then \
		echo "Using existing executables in bin/ (ensuring +x permissions)..."; \
		chmod +x bin/geofence-lib-test bin/geofence-processor 2>/dev/null || true; \
	else \
		echo "No application implementation found yet (RED specification mode)."; \
	fi

build-image:
	@if [ -f Dockerfile ]; then \
		echo "Building Docker image $(LOCAL_TAG)..."; \
		docker build -t $(LOCAL_TAG) .; \
	else \
		echo "No Dockerfile found yet (RED specification mode)."; \
	fi

# ---------------------------------------------------------------------------
# Workshop Phase Checkpoints
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
	@echo "Restoring reference Error Path Enumeration and Feature Files (Phase 2/3 complete -> ready for Phase 4)..."
	git checkout HEAD -- bdd/00_error_path_enumeration.md bdd/mi1_geofence_library.feature bdd/mi2_geofence_processor.feature bdd/mi3_geofence_processor_image.feature bdd/mi4_cloud_run.feature
	@echo "Reference Feature Files restored in bdd/."

checkpoint-steps: checkpoint-features
	@echo "Restoring reference Step Definitions and burning application code (Phase 4 complete -> ready for Phase 5)..."
	git checkout HEAD -- bdd/steps/ bdd/environment.py
	rm -rf $(BURN_PATHS)
	@echo "Specification and Steps ready (RED). Application code removed."
	@echo "Run 'make test-mi1' to verify RED state, then use prompts/05-autonomous-implementation.md!"

burn: checkpoint-steps

restore-all:
	@echo "Restoring complete reference workspace (Spec + Steps + Go implementation)..."
	rm -rf $(BURN_PATHS)
	git checkout HEAD -- governance/ bdd/ cmd/ internal/ go.mod go.sum Dockerfile Makefile
	@echo "Workspace restored."

# ---------------------------------------------------------------------------
# Emulator lifecycle
# Firestore: npx firebase-tools (uses host Node.js + downloads JAR once)
# Pub/Sub:   Docker container
# ---------------------------------------------------------------------------

start-emulators:
	@echo "Starting Firestore emulator..."
	@mkdir -p $(EMULATOR_FIRESTORE_DIR)
	@printf '{"emulators":{"firestore":{"port":8082,"host":"localhost"},"ui":{"enabled":false}}}' \
		> $(EMULATOR_FIRESTORE_DIR)/firebase.json
	@cd $(EMULATOR_FIRESTORE_DIR) && \
		nohup npx --yes firebase-tools@15.11.0 emulators:start \
			--only firestore --project equiguard-test \
			> $(EMULATOR_FIRESTORE_DIR)/firestore.log 2>&1 & \
		echo $$! > $(EMULATOR_FIRESTORE_PID)
	@echo "Starting Pub/Sub emulator..."
	-docker rm -f $(EMULATOR_PUBSUB_NAME) 2>/dev/null
	docker run -d --name $(EMULATOR_PUBSUB_NAME) \
		-p 8085:8085 $(EMULATOR_PUBSUB_IMAGE) \
		gcloud beta emulators pubsub start --host-port=0.0.0.0:8085
	@echo "Waiting for Firestore emulator on :8082..."
	@until curl -sf http://localhost:8082 >/dev/null 2>&1 || \
	        grep -q "Emulator Hub running" $(EMULATOR_FIRESTORE_DIR)/firestore.log 2>/dev/null; \
	 do sleep 1; done
	@echo "Waiting for Pub/Sub emulator on :8085..."
	@until curl -sf http://localhost:8085 >/dev/null 2>&1; do sleep 1; done
	@echo "Emulators ready."

stop-emulators:
	@if [ -f $(EMULATOR_FIRESTORE_PID) ]; then \
		kill $$(cat $(EMULATOR_FIRESTORE_PID)) 2>/dev/null || true; \
		rm -f $(EMULATOR_FIRESTORE_PID); \
	fi
	@docker stop $(EMULATOR_PUBSUB_NAME) 2>/dev/null || true
	@docker rm   $(EMULATOR_PUBSUB_NAME) 2>/dev/null || true
	@echo "Emulators stopped."

# ---------------------------------------------------------------------------
# Local BDD tests (MI1 – MI3)
# Each test target manages its own emulator lifecycle where needed.
# ---------------------------------------------------------------------------

test-mi1: build
	@echo "=== Milestone 1: Geofence Library ==="
	@bash -c "source .venv/bin/activate && behave bdd/ --tags=@mi1"

test-mi2: build start-emulators
	@echo "=== Milestone 2: Geofence Processor (Emulators) ==="
	@bash -c "source .venv/bin/activate && behave bdd/ --tags=@mi2"; \
	 status=$$?; $(MAKE) --no-print-directory stop-emulators; exit $$status

test-mi3: build build-image start-emulators
	@echo "=== Milestone 3: OCI Image ==="
	@bash -c "source .venv/bin/activate && behave bdd/ --tags=@mi3"; \
	 status=$$?; $(MAKE) --no-print-directory stop-emulators; exit $$status

test-all: build build-image start-emulators
	@echo "=== Running MI1 + MI2 + MI3 ==="
	@bash -c "source .venv/bin/activate && behave bdd/ --tags='@mi1 or @mi2 or @mi3'"; \
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
	@bash -c "source .venv/bin/activate && behave bdd/ --tags=@mi4 -D project_id=$(PROJECT)"

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
