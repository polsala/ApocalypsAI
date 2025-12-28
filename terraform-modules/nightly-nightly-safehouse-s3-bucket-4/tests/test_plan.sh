#!/usr/bin/env bash\n# Mock rationale: Use local backend and dummy credentials to validate configuration without real AWS calls.\n\nset -e\n\n# Initialize Terraform with no backend (local)\nterraform init -backend=false > /dev/null\n\n# Validate configuration\nterraform validate\n\n# Run a plan with dummy variables, expecting no errors\nterraform plan -var 'bucket_name=test-safehouse-bucket' \
  -var 'aws_region=us-east-1' \
  -var 'aws_access_key=FAKEACCESSKEY' \
  -var 'aws_secret_key=FAKESECRETKEY' \
  -out=plan.out > /dev/null\n\necho "Terraform plan succeeded."
