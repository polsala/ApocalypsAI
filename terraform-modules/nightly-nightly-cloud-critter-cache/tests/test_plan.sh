#!/bin/bash
set -euo pipefail

echo "--- Initializing Terraform ---"
terraform -chdir=tests init -backend=false # Mock rationale: -backend=false avoids needing a real backend

echo "--- Running Terraform Plan ---"
# Mock rationale: -no-color for consistent output, -out to save the plan for inspection
terraform -chdir=tests plan -out=tfplan -no-color

echo "--- Showing Terraform Plan JSON ---"
# Mock rationale: 'terraform show -json' provides a machine-readable, deterministic output of the plan.
# This allows for offline assertion without actual cloud interaction.
PLAN_JSON=$(terraform -chdir=tests show -json tfplan)

echo "--- Asserting S3 Bucket Resource ---"
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket" and .change.actions[] == "create")'; then
  echo "Test failed: aws_s3_bucket resource not found in plan or not marked for creation."
  exit 1
fi
echo "Assertion passed: aws_s3_bucket resource found."

echo "--- Asserting S3 Bucket Public Access Block Resource ---"
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_public_access_block" and .change.actions[] == "create")'; then
  echo "Test failed: aws_s3_bucket_public_access_block resource not found in plan or not marked for creation."
  exit 1
fi
echo "Assertion passed: aws_s3_bucket_public_access_block resource found."

echo "--- Asserting S3 Bucket Object Resource ---"
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_object" and .change.actions[] == "create")'; then
  echo "Test failed: aws_s3_bucket_object resource not found in plan or not marked for creation."
  exit 1
fi
echo "Assertion passed: aws_s3_bucket_object resource found."

echo "--- Asserting Bucket Name Prefix ---"
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket" and .change.after.bucket_prefix == "test-critter-cache-")'; then
  echo "Test failed: S3 bucket prefix 'test-critter-cache-' not found in plan."
  exit 1
fi
echo "Assertion passed: S3 bucket prefix is correct."

echo "--- Asserting Critter Name Tag ---"
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket" and .change.after.tags.CritterName == "TestCritter")'; then
  echo "Test failed: CritterName tag 'TestCritter' not found in plan."
  exit 1
fi
echo "Assertion passed: CritterName tag is correct."

echo "--- Asserting Comfort Message Content ---"
if ! echo "$PLAN_JSON" | jq -e '.resource_changes[] | select(.type == "aws_s3_bucket_object" and .change.after.content == "Beep boop, you're loved!")'; then
  echo "Test failed: Comfort message content 'Beep boop, you're loved!' not found in plan."
  exit 1
fi
echo "Assertion passed: Comfort message content is correct."

echo "All Terraform plan assertions passed!"
