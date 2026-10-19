#!/usr/bin/env bash
set -e

# Initialize Terraform in the module directory without a backend (offline mode)
terraform -chdir=src init -backend=false > /dev/null

# Validate the configuration; this will fail if there are syntax errors or missing required arguments
terraform -chdir=src validate -no-color

# Mock rationale: This test runs `terraform validate` with a mocked AWS provider that skips credential and metadata checks, ensuring the module is syntactically correct without contacting any external services.
