# Nightly Digital Time Capsule

A whimsical-yet-useful Terraform module to provision a secure, versioned AWS S3 bucket for storing a digital time capsule. This module ensures your precious data, messages to the future, or apocalyptic wisdom is safely archived with versioning, encryption, and lifecycle management.

## Features

*   **Secure Storage**: Provisions an AWS S3 bucket with all public access blocked by default.
*   **Versioning**: Automatically enabled to keep a history of all changes to your time capsule contents.
*   **Encryption**: Server-side encryption (AES256) is enforced for all objects.
*   **Lifecycle Management**: Configures rules to transition old versions to AWS Glacier for cost-effective long-term archival and eventually expire them after a defined period.
*   **Random Suffix**: Appends a random string to the bucket name to help ensure global uniqueness.

## Usage

To use this module, include it in your Terraform configuration:

```terraform
module "my_time_capsule" {
  source = "github.com/polsala/ApocalypsAI//terraform-modules/nightly-digital-time-capsule/src"

  # Optional: Customize the bucket name prefix
  bucket_name_prefix = "my-community-archive-"

  # Optional: Disable versioning if not desired (default is true)
  enable_versioning = true

  # Optional: Adjust days for Glacier transition (default: 365 days)
  glacier_transition_days = 730 # 2 years

  # Optional: Adjust days for object expiration (default: 1825 days / 5 years)
  expiration_days = 3650 # 10 years

  # Ensure your AWS provider is configured
  # provider "aws" {
  #   region = "us-east-1"
  # }
}

output "time_capsule_bucket_name" {
  description = "The name of the created S3 bucket."
  value       = module.my_time_capsule.bucket_id
}

output "time_capsule_bucket_arn" {
  description = "The ARN of the created S3 bucket."
  value       = module.my_time_capsule.bucket_arn
}
```

### Requirements

*   [Terraform](https://www.terraform.io/downloads.html) (v1.0.0 or higher)
*   Configured AWS credentials (e.g., via `~/.aws/credentials` or environment variables)

## Module Inputs

| Name                      | Description                                                                 | Type     | Default                      | Required |
| :------------------------ | :-------------------------------------------------------------------------- | :------- | :--------------------------- | :------- |
| `bucket_name_prefix`      | Prefix for the S3 bucket name. A random suffix will be appended.            | `string` | `"apocalypsai-time-capsule-"` | no       |
| `region`                  | AWS region where the S3 bucket will be created.                             | `string` | `"us-east-1"`                | no       |
| `enable_versioning`       | Whether to enable versioning for the S3 bucket.                             | `bool`   | `true`                       | no       |
| `glacier_transition_days` | Days after which objects (and non-current versions) transition to GLACIER.  | `number` | `365`                        | no       |
| `expiration_days`         | Days after which objects (and non-current versions) expire and are deleted. | `number` | `1825`                       | no       |

## Module Outputs

| Name                          | Description                                   |
| :---------------------------- | :-------------------------------------------- |
| `bucket_id`                   | The ID (name) of the S3 bucket.               |
| `bucket_arn`                  | The ARN of the S3 bucket.                     |
| `bucket_regional_domain_name` | The regional domain name of the S3 bucket.    |

## Development and Testing

This module includes automated tests to ensure its functionality and adherence to security best practices.

### Prerequisites for Testing

*   [Terraform](https://www.terraform.io/downloads.html)
*   [jq](https://stedolan.github.io/jq/download/) (for parsing JSON output in tests)
*   Bash shell

### Running Tests

Navigate to the `tests/` directory and execute the `test.sh` script:

```bash
cd tests/
./test.sh
```

The `test.sh` script performs the following:
1.  Initializes Terraform in an offline mode (`-backend=false`).
2.  Validates the Terraform configuration for syntax and consistency.
3.  Generates an execution plan (`terraform plan -out=tfplan`).
4.  Inspects the JSON output of the plan (`terraform show -json tfplan`) to assert that:
    *   An `aws_s3_bucket` resource is planned for creation.
    *   Versioning is enabled.
    *   All public access blocking settings are `true`.
    *   Server-side encryption (AES256) is configured.
    *   The lifecycle rule with specified transition and expiration days is present.

This approach ensures deterministic and offline testing, verifying the module's intended behavior without provisioning actual cloud resources.
