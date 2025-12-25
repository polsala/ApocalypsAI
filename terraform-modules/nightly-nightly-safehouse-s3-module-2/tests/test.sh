#!/usr/bin/env bash
set -e

# Initialise Terraform without a remote backend
terraform init -backend=false -input=false > /dev/null

# Validate the configuration syntax
terraform validate

# Execute a deterministic plan using a fixed bucket name
terraform plan -input=false -var="bucket_name=nightly-safehouse-demo" -out=plan.out > /dev/null

echo "All Terraform checks passed."
