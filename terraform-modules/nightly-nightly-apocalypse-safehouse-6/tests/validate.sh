#!/usr/bin/env bash
set -e

# Initialize the module without a remote backend
terraform init -backend=false -input=false > /dev/null

# Ensure all files are properly formatted
terraform fmt -check -recursive > /dev/null

# Validate the configuration syntax
terraform validate > /dev/null

# Mock rationale: In CI we assume provider plugins are cached, so no network calls are performed.

echo "All Terraform checks passed."
