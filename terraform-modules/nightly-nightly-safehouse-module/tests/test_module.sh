#!/usr/bin/env bash
set -e

# Initialize Terraform in offline mode (no backend)
terraform init -backend=false > /dev/null

# Validate configuration
terraform validate

# Apply the module (creates mock resources only)
terraform apply -auto-approve -input=false > /dev/null

# Verify that the output file was created
EXPECTED_FILE=$(ls shelter_*.txt | head -n1)
if [[ -f "$EXPECTED_FILE" ]]; then
  echo "Test passed: $EXPECTED_FILE created."
else
  echo "Test failed: shelter file not found."
  exit 1
fi

# Destroy resources
terraform destroy -auto-approve -input=false > /dev/null

# Clean up generated files
rm -f shelter_*.txt

# Mock rationale: All resources are local (null/random), no external calls, suitable for offline CI.
