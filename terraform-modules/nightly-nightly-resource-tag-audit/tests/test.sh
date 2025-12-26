#!/bin/bash
set -euo pipefail

# Mock rationale: This test script runs Terraform in an isolated, local context.
# The module itself is designed to process input variables and produce outputs purely through HCL logic,
# without making any actual AWS API calls. 'terraform apply' in this test setup merely computes
# these outputs locally based on the mock inputs provided in tests/main.tf, ensuring determinism and offline execution.

echo "Running Nightly Resource Tag Audit module tests..."

# Check for jq dependency
if ! command -v jq &> /dev/null
then
    echo "Error: 'jq' is not installed. Please install it to run these tests." >&2
    exit 1
fi

# Initialize Terraform in the test directory
echo "Initializing Terraform..."
terraform -chdir=tests init -backend=false # -backend=false ensures no remote state backend is configured
if [ $? -ne 0 ]; then
  echo "Terraform initialization failed!" >&2
  exit 1
fi

# Validate Terraform configuration syntax
echo "Validating Terraform configuration..."
terraform -chdir=tests validate
if [ $? -ne 0 ]; then
  echo "Terraform validation failed!" >&2
  exit 1
fi

# Run terraform apply to compute the module's outputs locally
# The module does not create real cloud resources, so apply is safe and offline.
echo "Applying test configuration to compute outputs..."
terraform -chdir=tests apply -auto-approve -json > tests/apply_output.json
if [ $? -ne 0 ]; then
  echo "Terraform apply failed!" >&2
  exit 1
fi

# Extract the audit_report output using jq
AUDIT_REPORT_JSON=$(jq -c '.outputs.tag_audit_test.value' tests/apply_output.json)

# Expected audit report based on tests/main.tf and required_tags:
# Resource 1: arn:aws:s3:::my-bucket-1, tags: { "Environment" = "prod", "Owner" = "ApocalypsAI" }
#   Required: { "Environment" = "", "Owner" = "ApocalypsAI", "Project" = "" }
#   Missing: "Project"

# Resource 2: arn:aws:ec2:us-east-1:123456789012:instance/i-0abcdef1234567890, tags: { "Environment" = "dev" }
#   Required: { "Environment" = "", "Owner" = "ApocalypsAI", "Project" = "" }
#   Missing: "Owner", "Project"

# Resource 3: arn:aws:s3:::my-bucket-2, tags: {}
#   Required: { "Environment" = "", "Owner" = "ApocalypsAI", "Project" = "" }
#   Missing: "Environment", "Owner", "Project"

# Resource 4: arn:aws:lambda:us-west-2:123456789012:function:my-function, tags: { "Environment" = "prod", "Owner" = "ApocalypsAI", "Project" = "Alpha" }
#   Required: { "Environment" = "", "Owner" = "ApocalypsAI", "Project" = "" }
#   Missing: None (Project value "Alpha" is fine as required_tags["Project"] is "")

# Expected number of non-compliant resources
EXPECTED_COUNT=3
ACTUAL_COUNT=$(echo "$AUDIT_REPORT_JSON" | jq 'length')

if [ "$ACTUAL_COUNT" -ne "$EXPECTED_COUNT" ]; then
  echo "Test failed: Expected $EXPECTED_COUNT non-compliant resources, but got $ACTUAL_COUNT." >&2
  echo "Full Audit Report: $AUDIT_REPORT_JSON" >&2
  exit 1
fi

# Check for specific missing tags for each expected non-compliant resource

# Test Case 1: my-bucket-1 should be missing 'Project'
if ! echo "$AUDIT_REPORT_JSON" | jq -e '.[] | select(.arn == "arn:aws:s3:::my-bucket-1" and (.missing_tag_keys | contains(["Project"])) and (.missing_tag_keys | length == 1))' > /dev/null; then
  echo "Test failed: arn:aws:s3:::my-bucket-1 did not report 'Project' as missing or reported other tags." >&2
  echo "Full Audit Report: $AUDIT_REPORT_JSON" >&2
  exit 1
fi

# Test Case 2: ec2 instance should be missing 'Owner' and 'Project'
if ! echo "$AUDIT_REPORT_JSON" | jq -e '.[] | select(.arn == "arn:aws:ec2:us-east-1:123456789012:instance/i-0abcdef1234567890" and (.missing_tag_keys | contains(["Owner", "Project"])) and (.missing_tag_keys | length == 2))' > /dev/null; then
  echo "Test failed: arn:aws:ec2:us-east-1:123456789012:instance/i-0abcdef1234567890 did not report 'Owner' and 'Project' as missing or reported other tags." >&2
  echo "Full Audit Report: $AUDIT_REPORT_JSON" >&2
  exit 1
fi

# Test Case 3: my-bucket-2 should be missing 'Environment', 'Owner', 'Project'
if ! echo "$AUDIT_REPORT_JSON" | jq -e '.[] | select(.arn == "arn:aws:s3:::my-bucket-2" and (.missing_tag_keys | contains(["Environment", "Owner", "Project"])) and (.missing_tag_keys | length == 3))' > /dev/null; then
  echo "Test failed: arn:aws:s3:::my-bucket-2 did not report 'Environment', 'Owner', and 'Project' as missing or reported other tags." >&2
  echo "Full Audit Report: $AUDIT_REPORT_JSON" >&2
  exit 1
fi

echo "All Nightly Resource Tag Audit tests passed successfully!"

# Clean up generated files
rm tests/apply_output.json
terraform -chdir=tests destroy -auto-approve > /dev/null # Clean up state, though no real resources were created.
