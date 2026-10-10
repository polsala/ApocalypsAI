#!/bin/bash
set -euo pipefail

echo "Running Terraform module tests..."

# Mock rationale: Terraform validate is an offline, deterministic check of HCL syntax.
# For a module, this is the primary "unit test" equivalent. It ensures the configuration
# is syntactically correct and internally consistent without needing AWS credentials
# or making any API calls. We cannot run `terraform plan` or `terraform apply` without
# AWS credentials, which would violate the "offline" and "deterministic" requirements
# for this agent. Therefore, we focus on validating the HCL syntax and structure,
# and verifying the presence of all expected source files.

# Navigate to the module directory
cd src

# Initialize Terraform (required before validate)
# -backend=false ensures no remote state interaction, making it offline.
echo "Initializing Terraform..."
terraform init -backend=false
if [ $? -ne 0 ]; then
    echo "Terraform init failed!"
    exit 1
fi
echo "Terraform init successful."

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate
if [ $? -ne 0 ]; then
    echo "Terraform validation failed!"
    exit 1
fi
echo "Terraform validation successful."

# Check for existence of key files (basic structural integrity)
echo "Checking for essential files..."
if [ ! -f "main.tf" ]; then
    echo "Error: main.tf not found."
    exit 1
fi
if [ ! -f "variables.tf" ]; then
    echo "Error: variables.tf not found."
    exit 1
fi
if [ ! -f "outputs.tf" ]; then
    echo "Error: outputs.tf not found."
    exit 1
fi
if [ ! -f "lambda/whisper_processor.py" ]; then
    echo "Error: lambda/whisper_processor.py not found."
    exit 1
fi
if [ ! -f "web/index.html" ]; then
    echo "Error: web/index.html not found."
    exit 1
fi
echo "All essential files found."

echo "Terraform module tests passed successfully!"
