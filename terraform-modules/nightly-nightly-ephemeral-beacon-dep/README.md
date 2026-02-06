# Nightly Ephemeral Beacon Deployer

## Summary
Deploys a minimal, ephemeral AWS S3 bucket beacon to broadcast a 'whisper' (a small text message) to the digital void. This utility is designed for quick deployment and easy teardown, perfect for sending fleeting messages or marking a temporary presence in the cloud.

## Classifier
`terraform-modules`

## Description
The `nightly-ephemeral-beacon-deployer` Terraform module provisions an AWS S3 bucket configured for public read access, and places a customizable `whisper.txt` file within it. This allows anyone with the bucket's public URL to retrieve the message. It's ideal for:
- Sending a quick, public, and ephemeral message.
- Marking a temporary point of interest in the cloud.
- Testing basic S3 public access configurations.

**Warning**: This module configures an S3 bucket and an object within it for public read access. Ensure you understand the implications of public data exposure before deploying. Only store non-sensitive information.

## Usage

### Prerequisites
-   [Terraform](https://www.terraform.io/downloads.html) installed (v1.0.0 or higher).
-   AWS credentials configured (e.g., via `~/.aws/credentials` or environment variables). The user/role associated with these credentials must have permissions to create S3 buckets, bucket policies, public access blocks, and objects.

### Deploying a Beacon

1.  Create a new directory for your deployment (e.g., `my-beacon`).
2.  Inside `my-beacon`, create a `main.tf` file:

    ```terraform
    # my-beacon/main.tf
    provider "aws" {
      region = "us-east-1" # Or your desired AWS region
    }

    module "my_ephemeral_beacon" {
      source = "path/to/nightly-ephemeral-beacon-deployer" # Adjust path if not local
      # For local testing, if this module is in a sibling directory:
      # source = "../nightly-ephemeral-beacon-deployer"

      bucket_name     = "apocalypsai-whisper-beacon-unique-id" # MUST be globally unique
      whisper_content = "The void whispers back: All is well, for now. Coordinates: [REDACTED]"
      aws_region      = "us-east-1" # Must match provider region
    }

    output "beacon_url" {
      value = module.my_ephemeral_beacon.beacon_whisper_url
    }
    ```

3.  Initialize Terraform:
    ```bash
    terraform init
    ```

4.  Review the plan:
    ```bash
    terraform plan
    ```

5.  Apply the changes to deploy your beacon:
    ```bash
    terraform apply
    ```
    Confirm with `yes` when prompted.

6.  After deployment, the `beacon_url` output will provide the public URL to your whisper.

### Destroying the Beacon

To remove all resources created by this module:

```bash
terraform destroy
```
Confirm with `yes` when prompted.

## Inputs

| Name              | Description                                                               | Type   | Default                                      | Required |
|-------------------|---------------------------------------------------------------------------|--------|----------------------------------------------|----------|
| `bucket_name`     | The unique name for the S3 bucket beacon.                                 | `string` | -                                            | yes      |
| `whisper_content` | The whimsical message or 'whisper' to store in the beacon.                | `string` | `"Hello from the void. All systems nominal..."` | no       |
| `aws_region`      | The AWS region to deploy the beacon. Must match the provider's region.    | `string` | `"us-east-1"`                                | no       |

## Outputs

| Name                 | Description                                              |
|----------------------|----------------------------------------------------------|
| `beacon_bucket_name` | The name of the S3 bucket beacon.                        |
| `beacon_whisper_url` | The public URL of the 'whisper' content in the S3 bucket.|

## Development & Testing

To run the automated tests for this module:

```bash
cd nightly-ephemeral-beacon-deployer/tests
./run_tests.sh
```

The `run_tests.sh` script performs `terraform init -backend=false`, `terraform validate`, and `terraform plan` on a test fixture (`test_beacon_deployment.tf`). This ensures the module's syntax is correct and its configuration is valid without requiring actual AWS credentials or deploying real resources. The `terraform plan` step verifies the expected resource creation and configuration.
