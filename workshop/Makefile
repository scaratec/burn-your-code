REGISTRY   := europe-west3-docker.pkg.dev
PROJECT    := randy-gupta-poc
REPO       := equiguard
IMAGE_NAME := geofence-processor
IMAGE_TAG  := v1
LOCAL_TAG  := equiguard/geofence-processor:test
REMOTE_TAG := $(REGISTRY)/$(PROJECT)/$(REPO)/$(IMAGE_NAME):$(IMAGE_TAG)

# Auto-detect Go binary — works regardless of installation path
GO := $(shell which go 2>/dev/null \
        || find /usr/local /opt/homebrew/bin -name go -type f 2>/dev/null \
           | head -1 \
        || echo go)

EMULATOR_PUBSUB_NAME    := equiguard-pubsub-emulator
EMULATOR_PUBSUB_IMAGE   := gcr.io/google.com/cloudsdktool/cloud-sdk:latest
EMULATOR_FIRESTORE_DIR  := /tmp/equiguard-emulators
EMULATOR_FIRESTORE_PID  := $(EMULATOR_FIRESTORE_DIR)/firestore.pid

.PHONY: help setup build build-image \
        start-emulators stop-emulators \
        test-mi1 test-mi2 test-mi3 test-mi4 test-all \
        auth-registry push-image \
        tf-init tf-apply teardown-mi4 \
        clean

# ---------------------------------------------------------------------------
# Default
# ---------------------------------------------------------------------------

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Local targets:"
	@echo "  setup            Install Python deps, resolve Go modules"
	@echo "  build            Compile Go binaries into bin/"
	@echo "  build-image      Build the geofence-processor Docker image"
	@echo "  start-emulators  Start Firestore (npx) + Pub/Sub (Docker) emulators"
	@echo "  stop-emulators   Stop and remove emulators"
	@echo "  test-mi1         Geofence Library (no infra needed)"
	@echo "  test-mi2         Processor Service (emulators managed automatically)"
	@echo "  test-mi3         OCI Image (emulators + Docker)"
	@echo "  test-all         Run MI1 + MI2 + MI3"
	@echo ""
	@echo "Cloud targets (MI4 — real GCP, incurs costs):"
	@echo "  auth-registry    Configure Docker for Artifact Registry"
	@echo "  push-image       Tag and push image to Artifact Registry"
	@echo "  tf-init          Initialize Terraform"
	@echo "  tf-apply         Provision all GCP resources via Terraform"
	@echo "  test-mi4         Run MI4 BDD tests against live Cloud Run"
	@echo "  teardown-mi4     Destroy all GCP resources (stops billing)"
	@echo ""
	@echo "  clean            Remove compiled binaries"

# ---------------------------------------------------------------------------
# Local setup
# ---------------------------------------------------------------------------

setup:
	@echo "Go binary: $(GO)"
	@$(GO) version
	@echo "Setting up Python virtual environment..."
	python3 -m venv .venv
	@bash -c "source .venv/bin/activate && \
		pip install -q behave requests \
		google-cloud-firestore google-cloud-pubsub"
	@echo "Resolving Go module dependencies..."
	$(GO) mod tidy
	@mkdir -p bin

build: setup
	@echo "Building Go binaries..."
	$(GO) build -o bin/geofence-processor ./cmd/geofence-processor/
	$(GO) build -o bin/geofence-lib-test  ./cmd/geofence-lib-test/
	@echo "Build complete."

build-image:
	@echo "Building Docker image $(LOCAL_TAG)..."
	docker build -t $(LOCAL_TAG) .
	@echo "Image built."

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
		nohup npx -y firebase-tools emulators:start \
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

test-mi3: build-image start-emulators
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

push-image: build-image auth-registry
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
	@echo "Provisioning GCP resources (project: $(PROJECT))..."
	terraform -chdir=terraform apply -auto-approve -input=false

# ---------------------------------------------------------------------------
# Cloud — MI4 BDD tests
# ---------------------------------------------------------------------------

test-mi4: setup
	@echo "=== Milestone 4: Cloud Run (LIVE GCP — project: $(PROJECT)) ==="
	@echo "WARNING: This test uses real GCP resources and incurs costs."
	@bash -c "source .venv/bin/activate && behave bdd/ --tags=@mi4"

# ---------------------------------------------------------------------------
# Teardown
# ---------------------------------------------------------------------------

teardown-mi4:
	@echo "Destroying all GCP resources for project $(PROJECT)..."
	@echo "This will delete: Cloud Run, Pub/Sub, Artifact Registry repository."
	@read -p "Are you sure? [y/N] " confirm && [ "$$confirm" = "y" ]
	terraform -chdir=terraform destroy -auto-approve -input=false
	@echo "Teardown complete."

# ---------------------------------------------------------------------------
# Clean
# ---------------------------------------------------------------------------

clean:
	@rm -rf bin/
	@echo "Cleaned."
