# Nightly Cloud Message Bottle

This Terraform module provisions an ephemeral AWS S3 bucket designed for secure, temporary message drops or small file transfers. Think of it as a digital message in a bottle, floating in the cloud, that automatically vanishes after a set period.

It's ideal for:
- Sharing sensitive, short-lived information between trusted parties.
- Temporary data exchange in automated workflows.
- A whimsical, self-cleaning cache for post-apocalyptic communiques.

## Features

- **Ephemeral Storage**: Objects are automatically deleted after a configurable number of days (default: 1 day).
- **Secure by Default**: Uses AWS S3 managed encryption (SSE-S3) and is private by default.
- **Simple Interface**: Easy to integrate into your existing Terraform configurations.

## Usage

To use this module, include it in your Terraform configuration:

```terraform
module "message_bottle" {
  source = "./nightly-cloud-message-bottle" # Adjust path if using from a different location

  bucket_name_prefix = "apocalypsai-message-drop"
  expiration_days    = 3 # Messages last for 3 days
  tags = {
    Project     = "ApocalypsAI"
    Environment = "Ephemeral"
    Purpose     = "MessageBottle"
  }
}

output "message_bottle_bucket_name" {
  description = "The name of the ephemeral S3 bucket."
  value       = module.message_bottle.bucket_id
}

output "message_bottle_bucket_arn" {
  description = "The ARN of the ephemeral S3 bucket."
  value       = module.message_bottle.bucket_arn
}
```

## Inputs

| Name                 | Description                                                                 | Type          | Default     | Required |
|----------------------|-----------------------------------------------------------------------------|---------------|-------------|----------|
| `bucket_name_prefix` | A unique prefix for the S3 bucket name. The module will append a random suffix. | `string`      | `""`        | yes      |
| `expiration_days`    | Number of days after which objects in the bucket will be automatically deleted. | `number`      | `1`         | no       |
| `tags`               | A map of tags to assign to the S3 bucket.                                   | `map(string)` | `{}`        | no       |

## Outputs

| Name                     | Description                               |
|--------------------------|-------------------------------------------|
| `bucket_id`              | The ID (name) of the created S3 bucket.   |
| `bucket_arn`             | The ARN of the created S3 bucket.         |
| `bucket_domain_name`     | The domain name of the created S3 bucket. |

## Requirements

- Terraform `~> 1.0`
- AWS Provider `~> 4.0`
- Configured AWS credentials (e.g., via environment variables, `~/.aws/credentials`, or IAM role).

## Development & Testing

To test this module locally:

1. Navigate to the `tests/` directory.
2. Run `terraform init`.
3. Run `terraform plan`. This will show you the resources that would be created without actually provisioning them.
   ```bash
   cd tests
   terraform init
   terraform plan
   ```
   Verify that the plan shows the creation of an `aws_s3_bucket` resource with the expected lifecycle rules and tags.
