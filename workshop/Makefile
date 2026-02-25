.PHONY: help test-mi1 test-mi2 test-all

# Default target
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  test-mi1   Run tests for Milestone 1 (Geofence Library)"
	@echo "  test-mi2   Run tests for Milestone 2 (Geofence Processor with Emulators)"
	@echo "  test-all   Run all tests"

test-mi1:
	@echo "Running Milestone 1 Tests (Library)..."
	@bash -c "source .venv/bin/activate && behave bdd/ --tags=@mi1"

test-mi2:
	@echo "Running Milestone 2 Tests (Processor)..."
	@bash -c "source .venv/bin/activate && behave bdd/ --tags=@mi2"

test-all:
	@echo "Running All Tests..."
	@bash -c "source .venv/bin/activate && behave bdd/"