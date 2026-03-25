.PHONY: help setup build test-mi1 test-mi2 test-mi3 test-all clean

# Default target
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  setup      Install Python deps and resolve Go module graph"
	@echo "  build      Compile Go binaries into bin/"
	@echo "  test-mi1   Run tests for Milestone 1 (Geofence Library)"
	@echo "  test-mi2   Run tests for Milestone 2 (Geofence Processor with Emulators)"
	@echo "  test-mi3   Run tests for Milestone 3 (OCI Image)"
	@echo "  test-all   Run all tests"
	@echo "  clean      Remove compiled binaries"

setup:
	@echo "Setting up Python virtual environment..."
	python3 -m venv .venv
	@bash -c "source .venv/bin/activate && pip install -q behave requests google-cloud-firestore"
	@echo "Resolving Go module dependencies..."
	go mod tidy
	@mkdir -p bin

build: setup
	@echo "Building Go binaries..."
	go build -o bin/geofence-processor ./cmd/geofence-processor/
	go build -o bin/geofence-lib-test ./cmd/geofence-lib-test/
	@echo "Build complete."

test-mi1: setup
	@echo "Running Milestone 1 Tests (Geofence Library)..."
	@bash -c "source .venv/bin/activate && behave bdd/ --tags=@mi1"

test-mi2: setup
	@echo "Running Milestone 2 Tests (Geofence Processor with Emulators)..."
	@bash -c "source .venv/bin/activate && behave bdd/ --tags=@mi2"

test-mi3: setup
	@echo "Running Milestone 3 Tests (OCI Image)..."
	@bash -c "source .venv/bin/activate && behave bdd/ --tags=@mi3"

test-all: setup
	@echo "Running All Tests..."
	@bash -c "source .venv/bin/activate && behave bdd/"

clean:
	@rm -rf bin/
	@echo "Cleaned."
