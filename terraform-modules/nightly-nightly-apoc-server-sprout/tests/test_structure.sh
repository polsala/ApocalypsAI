#!/bin/bash
# Mock rationale: Validates Terraform syntax without cloud access

terraform init -input=false || { echo 'Init failed'; exit 1; }
terraform validate || { echo 'Validation failed'; exit 1; }

test -f outputs.tf && test -s outputs.tf || { echo 'Empty outputs file'; exit 1; }
test -f variables.tf && grep -q 'survival_role' variables.tf || { echo 'Missing survival_role variable'; exit 1; }
