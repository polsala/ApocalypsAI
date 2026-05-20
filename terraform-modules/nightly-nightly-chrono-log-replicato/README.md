# Nightly Chrono-Log Replicator

## Summary
This Terraform module provisions a secure AWS S3 bucket and an associated IAM policy, designed for capturing and replicating 'chrono-logs' or temporal data streams. It provides a foundational 'echo chamber' for your critical time-sensitive data, enabling later analysis or replay.

## Usage
To use this module, include it in your Terraform configuration and provide the required variables. The module will create an S3 bucket with public access blocked by default and an IAM policy that grants `PutObject`, `GetObject`, and `ListBucket` permissions to the bucket. You can then attach this policy to an IAM role or user that needs to interact with the chrono-log bucket.

```terraform
module "chrono_log_replicator" {
  source = "./path/to/nightly-chrono-log-replicator/src" # Adjust path as needed

  bucket_name = "my-apocalypsai-chrono-logs-prod"
  environment = "production"
}

output "chrono_bucket_arn" {
  value = module.chrono_log_replicator.bucket_arn
}

output "chrono_iam_policy_arn" {
  value = module.chrono_log_replicator.iam_policy_arn
}
```

## Inputs

| Name        | Description                                                 | Type   | Default     | Required |
|-------------|-------------------------------------------------------------|--------|-------------|----------|
| `bucket_name` | The name of the S3 bucket for chrono-logs.                  | `string` | n/a         | yes      |
| `environment` | The environment tag for the S3 bucket (e.g., 'dev', 'prod'). | `string` | `"dev"`     | no       |

## Outputs

| Name              | Description                                              |
|-------------------|----------------------------------------------------------|
| `bucket_id`       | The ID of the created S3 bucket.                         |
| `bucket_arn`      | The ARN of the created S3 bucket.                        |
| `iam_policy_arn`  | The ARN of the IAM policy created for chrono-log write access. |

## Testing

To validate the module's syntax and structure without deploying actual resources, navigate to the `tests/` directory within the `nightly-chrono-log-replicator` utility folder and run:

```bash
terraform init
terraform validate
terraform plan -out=tfplan -no-color
```

These commands will verify that the module is correctly configured and can be planned, ensuring its integrity before any deployment.
