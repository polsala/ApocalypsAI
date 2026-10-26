# Nightly Temporal Echo Chamber Terraform Module

## Summary
This Terraform module provisions an AWS S3 bucket configured as a "Temporal Echo Chamber." It enables versioning and sets up lifecycle rules to transition older versions of objects to cheaper storage classes (like Glacier) and eventually expire them, simulating the fading of data "echoes" over time. It's a whimsical yet practical way to manage data retention and historical versions.

## Features
- Creates an AWS S3 bucket.
- Enables object versioning for historical data preservation.
- Configures lifecycle rules to automatically transition noncurrent object versions to GLACIER storage.
- Configures lifecycle rules to automatically expire noncurrent object versions after a specified period.

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

### Example

```terraform
module "my_echo_chamber" {
  source = "./path/to/nightly-temporal-echo-chamber-tf-module/src"

  bucket_name    = "my-apocalypsai-echo-chamber-bucket"
  aws_region     = "us-east-1" # Optional, defaults to us-east-1
  retention_days = 60          # Optional, defaults to 90 days
}

output "echo_chamber_bucket_arn" {
  value = module.my_echo_chamber.bucket_arn
}

output "echo_chamber_bucket_id" {
  value = module.my_echo_chamber.bucket_id
}
```

### Inputs

| Name           | Description                                                               | Type   | Default     | Required |
|----------------|---------------------------------------------------------------------------|--------|-------------|----------|
| `bucket_name`  | The name of the S3 bucket to create for the Temporal Echo Chamber.        | `string` | n/a         | yes      |
| `aws_region`   | The AWS region where the S3 bucket will be created.                       | `string` | `"us-east-1"` | no       |
| `retention_days` | Number of days after which noncurrent versions will transition to GLACIER storage class. | `number` | `90`        | no       |

### Outputs

| Name                | Description                      |
|---------------------|----------------------------------|
| `bucket_id`         | The ID (name) of the S3 bucket.  |
| `bucket_arn`        | The ARN of the S3 bucket.        |

## Requirements
- Terraform CLI (v1.0.0 or higher)
- AWS Provider configured (e.g., via AWS CLI or environment variables)

## Testing

To run the automated tests, navigate to the `tests/` directory and execute `test.sh`:

```bash
cd tests/
./test.sh
```

These tests perform `terraform init -backend=false`, `terraform validate`, and `terraform plan` to ensure the module's syntax and structure are correct without provisioning actual cloud resources.
