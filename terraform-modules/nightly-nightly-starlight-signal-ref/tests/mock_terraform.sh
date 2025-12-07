#!/bin/bash
# Mock rationale: Terraform commands (init, validate, apply, output) interact with the filesystem,
# download providers, and potentially communicate with cloud APIs. To ensure deterministic and
# offline testing, the 'terraform' binary is mocked. This mock simulates successful execution
# and predefined outputs, allowing the test script to verify the module's structure and
# expected behavior without actual cloud resource provisioning or network calls.

# This script acts as a mock for the 'terraform' CLI.
# It simulates the output of various terraform commands.

case "$1" in
  "init")
    echo "Terraform has been successfully initialized!"
    ;;
  "validate")
    echo "Success! The configuration is valid."
    ;;
  "apply")
    if [[ "$2" == "-auto-approve" ]]; then
      echo "Apply complete! Resources: 7 added, 0 changed, 0 destroyed."
    else
      echo "Error: -auto-approve not provided for mock apply."
      exit 1
    fi
    ;;
  "output")
    if [[ "$2" == "-json" && "$3" == "api_gateway_url" ]]; then
      echo "{\"api_gateway_url\": \"https://mock-api-gateway-url.execute-api.us-east-1.amazonaws.com/prod\"}"
    else
      echo "Error: Unexpected 'terraform output' arguments for mock."
      exit 1
    fi
    ;;
  "fmt")
    if [[ "$2" == "-check" ]]; then
      echo "" # Assume formatted correctly
    else
      echo "Error: Unexpected 'terraform fmt' arguments for mock."
      exit 1
    fi
    ;;
  *)
    echo "Error: Unknown terraform command: $1"
    exit 1
    ;;
esac
