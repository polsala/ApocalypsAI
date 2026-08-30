#!/bin/bash
set -euo pipefail

# Mock rationale: This test script uses `terraform validate` and `terraform plan`
# to ensure the module's syntax is correct and that it plans to create the expected
# resources with the correct tags. It does not actually provision AWS resources,
# making it deterministic and offline. `jq` is used to parse the plan output
# for specific assertions. Terraform's `random_pet` resource is also deterministic
# when run in `plan` mode without prior state, allowing consistent tag checks.

echo "--- Running Nightly Ephemeral Playground Terraform Module Tests ---"

# Check for required tools
if ! command -v terraform &> /dev/null; then
    echo "ERROR: terraform is not installed. Please install it to run tests."
    exit 1
fi
if ! command -v jq &> /dev/null; then
    echo "ERROR: jq is not installed. Please install it to run tests (e.g., sudo apt-get install jq)."
    exit 1
fi

# Create a temporary directory for testing
TEST_DIR=$(mktemp -d)
echo "Working in temporary directory: $TEST_DIR"
cp -R ../src/* "$TEST_DIR/"
cd "$TEST_DIR"

# Create a dummy public key file for testing
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC+G+dummykeyforapocalypsai+G+ dummy@example.com" > dummy_key.pub

# Create a test.tfvars file
cat <<EOF > test.tfvars
region = "us-east-1"
instance_type = "t2.micro"
ami_id = "ami-053b0d53c279acc90" # Amazon Linux 2 AMI (HVM), SSD Volume Type - us-east-1
key_name = "test-playground-key"
public_key_path = "dummy_key.pub"
destroy_after_hours = 1
EOF

# 1. Initialize Terraform (offline)
echo "1. Running terraform init..."
terraform init -backend=false > /dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: terraform init failed."
    exit 1
fi
echo "   terraform init successful."

# 2. Validate Terraform configuration
echo "2. Running terraform validate..."
terraform validate
if [ $? -ne 0 ]; then
    echo "ERROR: terraform validate failed."
    exit 1
fi
echo "   terraform validate successful."

# 3. Generate a plan and output as JSON
echo "3. Running terraform plan and capturing JSON output..."
terraform plan -var-file=test.tfvars -out=tfplan > /dev/null
terraform show -json tfplan > plan.json
if [ $? -ne 0 ]; then
    echo "ERROR: terraform plan failed."
    exit 1
fi
echo "   terraform plan successful, plan.json generated."

# 4. Assertions using jq
echo "4. Performing assertions on the generated plan..."

# Check for aws_instance resource
if ! jq -e '.resource_changes[] | select(.type == "aws_instance" and .change.actions[] == "create")' plan.json > /dev/null; then
    echo "ERROR: aws_instance resource not found in plan or not set for creation."
    exit 1
fi
echo "   - aws_instance resource found and set for creation."

# Check for EphemeralPlayground tag on instance
if ! jq -e '.resource_changes[] | select(.type == "aws_instance" and .change.after.tags.EphemeralPlayground == "true")' plan.json > /dev/null; then
    echo "ERROR: aws_instance does not have EphemeralPlayground tag set to 'true'."
    exit 1
fi
echo "   - aws_instance has EphemeralPlayground tag."

# Check for DestroyAfter tag on instance (presence and format)
if ! jq -e '.resource_changes[] | select(.type == "aws_instance" and .change.after.tags.DestroyAfter | test("^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$"))' plan.json > /dev/null; then
    echo "ERROR: aws_instance does not have DestroyAfter tag or it's not in expected format."
    exit 1
fi
echo "   - aws_instance has DestroyAfter tag in correct format."

# Check for aws_vpc resource
if ! jq -e '.resource_changes[] | select(.type == "aws_vpc" and .change.actions[] == "create")' plan.json > /dev/null; then
    echo "ERROR: aws_vpc resource not found in plan or not set for creation."
    exit 1
fi
echo "   - aws_vpc resource found and set for creation."

# Check for security group allowing port 22
if ! jq -e '.resource_changes[] | select(.type == "aws_security_group" and .change.after.ingress[] | select(.from_port == 22 and .to_port == 22 and .protocol == "tcp"))' plan.json > /dev/null; then
    echo "ERROR: aws_security_group does not allow ingress on port 22."
    exit 1
fi
echo "   - aws_security_group allows ingress on port 22."

echo "All tests passed successfully!"

# Clean up
cd - > /dev/null
rm -rf "$TEST_DIR"
echo "Cleaned up temporary directory: $TEST_DIR"
