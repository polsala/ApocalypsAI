#!/usr/bin/env bash
# Mock rationale: Simulate terraform commands without external dependencies.

tf_mock() {
  case "$1" in
    init)
      echo "Terraform has been successfully initialized!"
      return 0
      ;;
    validate)
      echo "Success! The configuration is valid."
      return 0
      ;;
    plan)
      echo "Plan: 1 to add, 0 to change, 0 to destroy."
      return 0
      ;;
    *)
      echo "Mock terraform: unknown command $1"
      return 1
      ;;
  esac
}

# Override the real terraform binary with our mock for the duration of the test
export -f tf_mock
alias terraform='tf_mock'

set -e

echo "Running mock terraform init..."
terraform init -backend=false

echo "Running mock terraform validate..."
terraform validate

echo "Running mock terraform plan..."
terraform plan -out=plan.out

echo "All mock terraform steps passed."
