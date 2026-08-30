# Nightly Stardust Harvester

A Terraform module designed to provision a whimsical, yet highly practical, AWS S3 bucket. This "Stardust Harvester" is optimized for collecting small, ephemeral, and potentially valuable data fragments (our "stardust") from various sources across your infrastructure. It includes sensible lifecycle rules to manage costs and optional SNS notifications to alert you when new stardust arrives or departs.

## Features

*   **Cost-Optimized Storage**: Configures lifecycle rules to automatically transition older objects to `STANDARD_IA` (Infrequent Access) and eventually expire them, keeping your storage costs low.
*   **Versioning**: Optionally enables S3 object versioning to protect against accidental deletions or overwrites.
*   **Public Access Block**: Ensures the bucket is private and blocks all public access by default.
*   **Incomplete Multipart Upload Abort**: Cleans up incomplete multipart uploads to prevent orphaned data and associated costs.
*   **Optional Notifications**: Integrates with AWS SNS to send notifications for object creation and deletion events, allowing you to react to your collected "stardust" in real-time.

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

```terraform
module "my_stardust_collector" {
  source = "./path/to/nightly-stardust-harvester" # Adjust path as needed

  bucket_prefix = "my-app-logs" # A unique prefix for your S3 bucket
  environment   = "production"

  # Optional settings (defaults are sensible)
  enable_versioning              = true
  transition_to_ia_days          = 45  # Transition to IA after 45 days
  expire_objects_days            = 180 # Expire objects after 180 days
  abort_incomplete_multipart_upload_days = 14 # Abort incomplete uploads after 14 days

  enable_notifications         = true
  notification_filter_prefix   = "important-events/" # Only notify for objects with this prefix
}

output "stardust_bucket_name" {
  value = module.my_stardust_collector.s3_bucket_id
}

output "stardust_notification_topic_arn" {
  value = module.my_stardust_collector.sns_topic_arn
}
```

## Inputs

| Name                                   | Description                                                               | Type     | Default     | Required |
| :------------------------------------- | :------------------------------------------------------------------------ | :------- | :---------- | :------- |
| `bucket_prefix`                        | A unique prefix for the S3 bucket name.                                   | `string` | `n/a`       | yes      |
| `environment`                          | The environment tag for resources.                                        | `string` | `"dev"`     | no       |
| `enable_versioning`                    | Enable versioning for the S3 bucket.                                      | `bool`   | `true`      | no       |
| `transition_to_ia_days`                | Number of days after which to transition objects to STANDARD_IA storage class. | `number` | `30`        | no       |
| `expire_objects_days`                  | Number of days after which to expire objects.                             | `number` | `90`        | no       |
| `abort_incomplete_multipart_upload_days` | Number of days after which to abort incomplete multipart uploads.         | `number` | `7`         | no       |
| `enable_notifications`                 | Enable SNS notifications for object events.                               | `bool`   | `false`     | no       |
| `notification_filter_prefix`           | Prefix to filter S3 object notifications (e.g., 'logs/').                 | `string` | `""`        | no       |

## Outputs

| Name                | Description                               | Value                                                               |
| :------------------ | :---------------------------------------- | :------------------------------------------------------------------ |
| `s3_bucket_id`      | The ID of the S3 bucket.                  | `aws_s3_bucket.stardust_bucket.id`                                  |
| `s3_bucket_arn`     | The ARN of the S3 bucket.                 | `aws_s3_bucket.stardust_bucket.arn`                                 |
| `sns_topic_arn`     | The ARN of the SNS topic (if enabled).    | `aws_sns_topic.stardust_notification_topic[0].arn` (or `null`)      |

## Testing

To run the automated tests for this module, navigate to the `tests/` directory and execute the `test.sh` script.

```bash
cd nightly-stardust-harvester/tests
./test.sh
```

The tests perform an offline `terraform init -backend=false`, `terraform validate`, and `terraform plan -destroy` to ensure the module's syntax is correct and it can generate a valid plan without interacting with a live AWS environment.
