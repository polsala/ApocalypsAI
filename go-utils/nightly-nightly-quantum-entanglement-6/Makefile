GOOS ?= $(shell go env GOOS)
GOARCH ?= $(shell go env GOARCH)
BINARY_NAME = nightly-quantum-entanglement-checker
VERSION = $(shell git describe --tags --always 2>/dev/null || echo "dev")
BUILD_TIME = $(shell date -u '+%Y-%m-%d_%H:%M:%S_UTC')
COMMIT_HASH = $(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown")

.PHONY: build install test clean help

# Default target
all: build

# Build the binary
build:
	@echo "Building $(BINARY_NAME) for $(GOOS)/$(GOARCH)..."
	@go build -o bin/$(BINARY_NAME) -ldflags "\
		-X 'main.version=$(VERSION)' \
		-X 'main.buildTime=$(BUILD_TIME)' \
		-X 'main.commitHash=$(COMMIT_HASH)'" ./src
	@echo "Build complete: bin/$(BINARY_NAME)"

# Install the binary globally
install: build
	@cp bin/$(BINARY_NAME) /usr/local/bin/
	@echo "Installed to /usr/local/bin/$(BINARY_NAME)"

# Run tests
test:
	@echo "Running tests..."
	@go test -v ./tests/...
	@echo "Tests complete"

# Clean build artifacts
clean:
	@rm -rf bin/
	@echo "Cleaned build artifacts"

# Show help
help:
	@echo "Available targets:"
	@echo "  build    - Build the binary"
	@echo "  install  - Install the binary globally"
	@echo "  test     - Run tests"
	@echo "  clean    - Clean build artifacts"
	@echo "  help     - Show this help"

# Create bin directory if it doesn't exist
bin/$(BINARY_NAME):
	@mkdir -p bin
