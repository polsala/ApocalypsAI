# Nightly Chrono-Cache

A Terraform module to provision a time-limited, auto-expiring cloud storage bucket for ephemeral data. Perfect for temporary logs, transient build artifacts, or fleeting messages that need to vanish after a set period.

## Features

*   **Ephemeral Storage**: Creates an AWS S3 bucket.
*   **Auto-Expiration**: Configures a lifecycle rule to automatically delete objects after a specified number of days.
*   **Secure by Default**: Private bucket access.
*   **Customizable**: Easily set bucket name prefix and expiration duration.

## Usage

To use this module, include it in your Terraform configuration:

```terraform
module "chrono_cache_bucket" {
  source = "./nightly-chrono-cache/src" # Adjust path if not in root
  
  bucket_name_prefix = "my-ephemeral-data"
  expiration_days    = 7 # Objects will expire after 7 days
  region             = "us-east-1" # Specify your desired AWS region
}

output "chrono_cache_bucket_id" {
  value = module.chrono_cache_bucket.bucket_id
}

output "chrono_cache_bucket_arn" {
  value = module.chrono_cache_bucket.bucket_arn
}
```

### Inputs

| Name                 | Description                                      | Type     | Default     | Required |
| :------------------- | :----------------------------------------------- | :------- | :---------- | :------- |
| `bucket_name_prefix` | A prefix for the S3 bucket name. A unique suffix will be added. | `string` | `"chrono-cache"` | no       |
| `expiration_days`    | Number of days after which objects in the bucket will expire. | `number` | `30`        | no       |
| `region`             | The AWS region to create the bucket in.          | `string` | n/a         | yes      |

### Outputs

| Name                | Description                     |
| :------------------ | :------------------------------ |
| `bucket_id`         | The ID (name) of the S3 bucket. |
| `bucket_arn`        | The ARN of the S3 bucket.       |

## Development & Testing

This module uses `terraform` for infrastructure provisioning.

### Prerequisites

*   Terraform CLI installed
*   AWS CLI configured (for actual deployment, not for tests)

### Running Tests

The tests validate the Terraform syntax and ensure a plan can be generated without actual cloud resource creation.

1.  Navigate to the `tests/` directory:
    ```bash
    cd tests
    ```
2.  Run the test script:
    ```bash
    ./test.sh
    ```

The `test.sh` script will:
*   Initialize Terraform.
*   Generate a `terraform plan` to verify the module's syntax and expected resource changes.
*   Clean up generated Terraform files.

**Mock rationale**: The `test.sh` script uses dummy AWS credentials (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`) to allow `terraform init` and `terraform plan` to run without attempting to authenticate against a real AWS account. This ensures the tests are deterministic, offline, and do not incur costs or require live infrastructure. The `terraform plan` command itself is sufficient to validate the HCL syntax and the module's structure.
