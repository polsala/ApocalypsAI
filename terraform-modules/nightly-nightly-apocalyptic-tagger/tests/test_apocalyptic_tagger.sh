#!/bin/bash
set -euo pipefail

echo "--- Running Nightly Apocalyptic Tagger Module Tests ---"

TEST_DIR=$(dirname "$0")
MODULE_DIR=$(realpath "$TEST_DIR/../src")

# Ensure Terraform is installed
if ! command -v terraform &> /dev/null
then
    echo "Terraform could not be found. Please install Terraform to run these tests."
    exit 1
fi

cd "$TEST_DIR"

echo "1. Initializing Terraform in $TEST_DIR..."
terraform init -backend=false # Mock rationale: -backend=false prevents state file creation, making it truly offline.
if [ $? -ne 0 ]; then
    echo "Terraform init failed!"
    exit 1
fi
echo "Terraform init successful."

echo "2. Running Terraform plan to validate module logic and outputs..."
PLAN_OUTPUT=$(terraform plan -no-color -input=false 2>&1)
if [ $? -ne 0 ]; then
    echo "Terraform plan failed!"
    echo "$PLAN_OUTPUT"
    exit 1
fi
echo "Terraform plan successful."

echo "3. Extracting and asserting outputs..."

# Mock rationale: Parsing plan output for expected strings is a deterministic,
# offline way to verify the module's computational logic without actual resource provisioning.

DEV_INSTANCE_NAME_EXPECTED="sentry-Echo-Chamber-Node-dev" # 'sentry' length 6, 6 % 8 = 6, index 6 of apocalypse_themes
PROD_DB_NAME_EXPECTED="data-vault-Void-Whisperer-prod" # 'data-vault' length 10, 10 % 8 = 2, index 2 of apocalypse_themes

# Check dev instance name
if echo "$PLAN_OUTPUT" | grep -q "dev_instance_name = \"$DEV_INSTANCE_NAME_EXPECTED\""; then
    echo "  ✅ Dev instance name matches expected: $DEV_INSTANCE_NAME_EXPECTED"
else
    echo "  ❌ Dev instance name MISMATCH. Expected: $DEV_INSTANCE_NAME_EXPECTED"
    echo "     Plan output snippet:"
    echo "$PLAN_OUTPUT" | grep "dev_instance_name" || true
    exit 1
fi

# Check prod DB name
if echo "$PLAN_OUTPUT" | grep -q "prod_db_name = \"$PROD_DB_NAME_EXPECTED\""; then
    echo "  ✅ Prod DB name matches expected: $PROD_DB_NAME_EXPECTED"
else
    echo "  ❌ Prod DB name MISMATCH. Expected: $PROD_DB_NAME_EXPECTED"
    echo "     Plan output snippet:"
    echo "$PLAN_OUTPUT" | grep "prod_db_name" || true
    exit 1
fi

# Check a specific tag for dev instance
if echo "$PLAN_OUTPUT" | grep -q "dev_instance_tags = {" && \
   echo "$PLAN_OUTPUT" | grep -q "ApocalypsePhase = \"Post-Collapse-Rebuild\"" && \
   echo "$PLAN_OUTPUT" | grep -q "Environment = \"dev\"" && \
   echo "$PLAN_OUTPUT" | grep -q "Purpose = \"EC2-Instance\""; then
    echo "  ✅ Dev instance tags contain expected values."
else
    echo "  ❌ Dev instance tags MISMATCH."
    echo "     Plan output snippet:"
    echo "$PLAN_OUTPUT" | grep "dev_instance_tags" -A 5 || true
    exit 1
fi

# Check a specific tag for prod DB
if echo "$PLAN_OUTPUT" | grep -q "prod_db_tags = {" && \
   echo "$PLAN_OUTPUT" | grep -q "ApocalypsePhase = \"Post-Collapse-Rebuild\"" && \
   echo "$PLAN_OUTPUT" | grep -q "Environment = \"prod\"" && \
   echo "$PLAN_OUTPUT" | grep -q "Purpose = \"RDS-DB\""; then
    echo "  ✅ Prod DB tags contain expected values."
else
    echo "  ❌ Prod DB tags MISMATCH."
    echo "     Plan output snippet:"
    echo "$PLAN_OUTPUT" | grep "prod_db_tags" -A 5 || true
    exit 1
fi

echo "All tests passed for Nightly Apocalyptic Tagger module!"
