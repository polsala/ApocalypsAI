#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODULE_DIR="${SCRIPT_DIR}/../src"

cd "$MODULE_DIR"
terraform init -backend=false > /dev/null
terraform validate
echo "Terraform validation passed"
