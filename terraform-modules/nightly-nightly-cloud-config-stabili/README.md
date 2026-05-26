# Nightly Cloud Config Stabilizer

## Overview

The `nightly-cloud-config-stabilizer` is a whimsical-yet-useful Terraform module designed to ensure the 'temporal stability' of critical cloud resources within the ApocalypsAI infrastructure. It defines a foundational resource (e.g., an S3 bucket for critical archives) and integrates a 'Cloud Configuration Stabilizer' – a `null_resource` with a `local-exec` provisioner – to simulate the detection and reporting of configuration drift, or 'configuration rifts'.

In a post-apocalyptic world, maintaining the integrity of your cloud infrastructure is paramount. This module helps you conceptualize and implement mechanisms to detect when your deployed resources deviate from their desired state, allowing for timely intervention by the IaC Chrono-Engineers.

## Features

*   **Critical Resource Definition**: Sets up a core cloud resource (currently an AWS S3 bucket).
*   **Configuration Rift Detection**: Employs a `null_resource` with `local-exec` to simulate an external drift detection system.
*   **Status Reporting**: Outputs a clear message indicating whether the resource is stable or if a 'configuration rift' has been detected.
*   **Extensible**: The drift detection mechanism can be extended to integrate with actual monitoring tools or cloud API checks.

## Usage

To use this module, include it in your Terraform configuration and provide the necessary variables.

### Prerequisites

*   Terraform CLI installed.
*   AWS CLI configured (though for testing, actual credentials are not strictly required as the provider is mocked).

### Example Configuration

Create a `main.tf` file in your root Terraform directory:

```terraform
# main.tf

# Configure the AWS provider (mocked for local testing)
provider "aws" {
  region = "us-east-1" # Example region
  # Mock rationale: For local, offline testing, actual AWS credentials are not needed.
  # The module's core logic (drift detection simulation) relies on the null_resource
  # and local-exec, which are self-contained. These mock values prevent Terraform
  # from complaining about missing credentials during 'terraform init' and 'plan'.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "apocalypsai_archive_stabilizer" {
  source = "./path/to/nightly-cloud-config-stabilizer/src"

  # Define a unique name for your critical archive bucket
  bucket_name = "my-critical-apocalypsai-archive-123"

  # Set this to "DRIFT_DETECTED" to simulate a configuration rift,
  # or leave as "STABLE" for a stable state.
  simulate_drift_signal = "STABLE" # or "DRIFT_DETECTED"
}

output "archive_status" {
  value       = module.apocalypsai_archive_stabilizer.stabilizer_status
  description = "The current status reported by the Cloud Configuration Stabilizer."
}

output "archive_bucket_name" {
  value       = module.apocalypsai_archive_stabilizer.archive_bucket_name
  description = "The name of the stabilized critical archive bucket."
}
```

### Running Terraform

1.  Initialize Terraform:
    ```bash
    terraform init
    ```
2.  Plan your infrastructure (this will trigger the stabilizer):
    ```bash
    terraform plan
    ```
    Observe the output from the `Cloud Configuration Stabilizer`.

3.  Apply changes (if you want to create the S3 bucket):
    ```bash
    terraform apply
    ```

## Testing

The module includes a `tests/test_stabilizer.sh` script that demonstrates how to run `terraform plan` with different `simulate_drift_signal` values to verify the drift detection logic offline and deterministically.

To run the tests:

```bash
./tests/test_stabilizer.sh
```

This script will create a temporary Terraform configuration, initialize it, and run `terraform plan` twice: once simulating a stable state and once simulating a drifted state, asserting on the expected output and exit codes.
