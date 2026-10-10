#!/usr/bin/env bash
# Mock rationale: This script runs terraform init and validate offline without contacting AWS.
set -e
cd "$(dirname "$0")/../src"
terraform init -backend=false > /dev/null
terraform validate > /dev/null
echo "Terraform configuration is valid."
