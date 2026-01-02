#!/bin/bash
set -euo pipefail

TEST_DIR="tests"

echo "Initializing Terraform in ${TEST_DIR}..."
terraform -chdir="${TEST_DIR}" init -backend=false # Mock rationale: -backend=false avoids needing a real backend

echo "Running terraform plan and capturing JSON output..."
PLAN_OUTPUT=$(terraform -chdir="${TEST_DIR}" plan -out=tfplan -json)
# Mock rationale: `terraform plan -json` allows us to inspect the planned changes
# without interacting with the actual AWS API, making the test offline and deterministic.
# We are asserting the structure and values of the planned resources.

if [ $? -ne 0 ]; then
    echo "Terraform plan failed!"
    echo "${PLAN_OUTPUT}"
    exit 1
fi

echo "Inspecting planned changes..."

# Check for aws_instance resource
INSTANCE_PLANNED=$(echo "${PLAN_OUTPUT}" | jq -r '.resource_changes[] | select(.type == "aws_instance" and .name == "critter_instance")')
if [ -z "${INSTANCE_PLANNED}" ]; then
    echo "Error: aws_instance.critter_instance not found in plan."
    exit 1
fi

# Check instance_type
INSTANCE_TYPE=$(echo "${INSTANCE_PLANNED}" | jq -r '.change.after.instance_type')
if [ "${INSTANCE_TYPE}" != "t3.nano" ]; then
    echo "Error: Expected instance_type 't3.nano', got '${INSTANCE_TYPE}'."
    exit 1
fi

# Check tags
INSTANCE_TAGS_NAME=$(echo "${INSTANCE_PLANNED}" | jq -r '.change.after.tags.Name')
if [ "${INSTANCE_TAGS_NAME}" != "CloudCritter-TestCritter" ]; then
    echo "Error: Expected instance tag Name 'CloudCritter-TestCritter', got '${INSTANCE_TAGS_NAME}'."
    exit 1
fi

# Check user_data content (simplified check for presence of critter_name)
USER_DATA_CONTENT=$(echo "${INSTANCE_PLANNED}" | jq -r '.change.after.user_data')
if [[ ! "${USER_DATA_CONTENT}" =~ "TestCritter" ]]; then
    echo "Error: user_data does not contain 'TestCritter' as expected."
    exit 1
fi


# Check for aws_security_group resource
SG_PLANNED=$(echo "${PLAN_OUTPUT}" | jq -r '.resource_changes[] | select(.type == "aws_security_group" and .name == "critter_sg")')
if [ -z "${SG_PLANNED}" ]; then
    echo "Error: aws_security_group.critter_sg not found in plan."
    exit 1
fi

# Check security group name
SG_NAME=$(echo "${SG_PLANNED}" | jq -r '.change.after.name')
if [ "${SG_NAME}" != "critter-security-group-TestCritter" ]; then
    echo "Error: Expected security group name 'critter-security-group-TestCritter', got '${SG_NAME}'."
    exit 1
}

# Check ingress rules (simplified check for presence, not full rule validation)
INGRESS_RULES=$(echo "${SG_PLANNED}" | jq -r '.change.after.ingress | length')
if [ "${INGRESS_RULES}" -lt 2 ]; then # Expecting at least 2 rules (SSH, HTTP)
    echo "Error: Expected at least 2 ingress rules, got ${INGRESS_RULES}."
    exit 1
fi

echo "All planned resource checks passed!"

# Check outputs
OUTPUTS_PLANNED=$(echo "${PLAN_OUTPUT}" | jq -r '.planned_values.outputs')
if [ -z "${OUTPUTS_PLANNED}" ]; then
    echo "Error: No outputs found in plan."
    exit 1
fi

# Check if outputs are present (their values will be unknown until apply, but we can check if they are planned)
if ! echo "${OUTPUTS_PLANNED}" | jq -e '.test_instance_public_ip' > /dev/null; then
    echo "Error: Output 'test_instance_public_ip' not found in plan."
    exit 1
fi
if ! echo "${OUTPUTS_PLANNED}" | jq -e '.test_instance_id' > /dev/null; then
    echo "Error: Output 'test_instance_id' not found in plan."
    exit 1
fi
if ! echo "${OUTPUTS_PLANNED}" | jq -e '.test_security_group_id' > /dev/null; then
    echo "Error: Output 'test_security_group_id' not found in plan."
    exit 1
fi

echo "All planned output checks passed!"
echo "Terraform module test completed successfully."

# Clean up generated plan file
rm tfplan
