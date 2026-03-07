#!/bin/bash
set -euo pipefail

echo "--- Running Terraform module tests ---"

# Mock rationale: These tests perform static analysis and content verification
# without requiring actual AWS credentials or network access, making them
# deterministic and offline.

# Navigate to the root of the utility for relative paths
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
cd "$SCRIPT_DIR/.."

# 1. Initialize Terraform in the test directory
echo "Initializing Terraform in tests/ directory..."
terraform -chdir=tests init -backend=false > /dev/null
echo "Terraform initialized successfully."

# 2. Validate the Terraform configuration for syntax and consistency
echo "Validating Terraform configuration in tests/ directory..."
terraform -chdir=tests validate
echo "Terraform configuration validated successfully."

# 3. Check Terraform formatting
echo "Checking Terraform formatting in tests/ directory..."
terraform -chdir=tests fmt -check
echo "Terraform formatting is correct."

# 4. Verify key configurations in the module's source files
echo "Verifying critical S3 bucket configurations in src/main.tf..."

# Check for versioning
grep -q 'status = "Enabled"' src/main.tf || { echo "Error: Versioning not enabled in src/main.tf"; exit 1; }
echo "Versioning configuration found."

# Check for server-side encryption
grep -q 'sse_algorithm = "AES256"' src/main.tf || { echo "Error: SSE-S3 encryption not configured in src/main.tf"; exit 1; }
echo "Server-side encryption configuration found."

# Check for public access block
grep -q 'block_public_acls       = true' src/main.tf || { echo "Error: Public ACL blocking not configured in src/main.tf"; exit 1; }
grep -q 'block_public_and_cross_account_access = true' src/main.tf || { echo "Error: Public and cross-account access blocking not configured in src/main.tf"; exit 1; }
echo "Public access block configuration found."

echo "All critical configurations verified."

echo "--- Terraform module tests passed! ---"
