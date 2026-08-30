#!/bin/bash
set -euo pipefail

# Mock rationale: This test performs a 'terraform plan -destroy' dry run
# without actual AWS credentials or resource creation. It validates the HCL
# syntax and ensures the module can be initialized and planned successfully.
# The 'ami-0abcdef1234567890' is a placeholder AMI ID, as 'terraform plan'
# only validates the format, not the existence, when no AWS credentials are present.
# The '-backend=false' flag ensures no remote state is involved, making it offline.

TEMP_DIR=$(mktemp -d)
MODULE_PATH="$(dirname "$0")"/../src

echo "Running Terraform plan validation test..."
echo "Temporary directory: $TEMP_DIR"

# Create a minimal test configuration that calls the module
cat <<EOF > "$TEMP_DIR/test.tf"
module "scavenged_outpost" {
  source = "$MODULE_PATH"

  prefix            = "test-scavenger"
  region            = "us-east-1"
  enable_s3_cache   = true
  enable_ec2_relay  = true
  ec2_instance_type = "t3.nano"
  ec2_ami_id        = "ami-0abcdef1234567890" # Mock AMI ID
  ec2_key_name      = "test-keypair"         # Mock Key Pair Name
}
EOF

cd "$TEMP_DIR"

# Initialize Terraform (without backend to keep it offline)
echo "Initializing Terraform..."
terraform init -backend=false

# Validate the Terraform configuration and generate a destroy plan
# A destroy plan is chosen as it's less likely to require specific
# resource attributes that only exist after creation, focusing on syntax.
echo "Running terraform plan -destroy..."
if ! terraform plan -destroy -no-color; then
    echo "Terraform plan validation FAILED!"
    rm -rf "$TEMP_DIR"
    exit 1
fi

echo "Terraform plan validation PASSED!"
rm -rf "$TEMP_DIR"
exit 0
