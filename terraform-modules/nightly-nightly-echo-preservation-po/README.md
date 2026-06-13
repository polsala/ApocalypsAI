# Nightly Echo Preservation Pod

This Terraform module provisions a secure AWS S3 bucket designed to act as a 'Temporal Echo Chamber' or 'Echo Preservation Pod'. It's configured with versioning, server-side encryption, and lifecycle rules to simulate temporal decay, moving older 'echoes' (objects) to Glacier and eventually deleting them.

## Features

*   **Unique Naming**: Generates a unique S3 bucket name based on provided prefix and environment.
*   **Secure by Default**: Enforces private ACLs, blocks public access, and enables server-side encryption (AES256).
*   **Versioning**: Keeps multiple versions of objects, crucial for 'temporal echoes'.
*   **Lifecycle Management**: Automatically transitions objects to Glacier after a configurable period and deletes them after another period, simulating data decay or archival.
*   **Tagging**: Applies standard and custom tags for better resource management.

## Usage

To use this module, include it in your Terraform configuration:

```terraform
module "my_echo_pod" {
  source = "./path/to/nightly-echo-preservation-pod/src"

  name_prefix           = "my-temporal-archive"
  environment           = "production"
  retention_days_standard = 60  # Move to Glacier after 60 days
  retention_days_glacier  = 730 # Delete after 730 days in Glacier (2 years total)
  tags = {
    "Project" = "ApocalypsAI"
    "Owner"   = "IntegratorAgent"
  }
}

output "echo_pod_bucket_name" {
  value = module.my_echo_pod.bucket_id
}
```

## Inputs

| Name                    | Description                                                               | Type     | Default             | Required |
| :---------------------- | :------------------------------------------------------------------------ | :------- | :------------------ | :------- |
| `name_prefix`           | A unique prefix for the S3 bucket name.                                   | `string` | `"echo-preservation"` | no       |
| `environment`           | The environment tag for the bucket (e.g., `dev`, `prod`, `staging`).      | `string` | `"dev"`               | no       |
| `retention_days_standard` | Number of days to keep objects in standard storage before moving to Glacier. | `number` | `30`                | no       |
| `retention_days_glacier`| Number of days to keep objects in Glacier before permanent deletion.      | `number` | `365`               | no       |
| `tags`                  | A map of tags to assign to the S3 bucket.                                 | `map(string)` | `{}`                | no       |

## Outputs

| Name                 | Description                               | Type     |
| :------------------- | :---------------------------------------- | :------- |
| `bucket_id`          | The ID (name) of the S3 bucket.           | `string` |
| `bucket_arn`         | The ARN of the S3 bucket.                 | `string` |
| `bucket_domain_name` | The S3 bucket domain name.                | `string` |

## Testing

To run the automated tests for this module, navigate to the `tests/` directory and execute the `test_module.sh` script:

```bash
cd nightly-echo-preservation-pod/tests
./test_module.sh
```

These tests perform offline validation of the Terraform configuration, ensuring syntax correctness and proper formatting without provisioning actual cloud resources.
