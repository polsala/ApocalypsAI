# nightly-digital-bottle-post

A whimsical-yet-useful Terraform module to provision a "Digital Message in a Bottle" AWS S3 bucket. This bucket is designed for ephemeral, publicly readable messages, perfect for sending digital notes into the void with a self-destruct timer.

## Features

*   **Ephemeral Storage**: Configurable lifecycle rules to automatically expire messages after a set duration.
*   **Public Read Access**: Optionally allows public read access for messages (default: private).
*   **Versioning**: Keeps track of message versions.
*   **Encryption**: Server-side encryption (SSE-S3) enabled by default.
*   **Tagging**: Customizable tags for resource organization.

## Usage

```terraform
module "digital_bottle_post" {
  source = "./path/to/nightly-digital-bottle-post" # Or a Git/Terraform Registry source

  bucket_name_prefix = "apocalypsai-bottle"
  message_retention_days = 7 # Messages expire after 7 days
  enable_public_read = true # Allow anyone to read messages
  tags = {
    Project = "ApocalypsAI"
    Purpose = "DigitalBottlePost"
  }
}

output "bucket_id" {
  value = module.digital_bottle_post.bucket_id
}

output "bucket_arn" {
  value = module.digital_bottle_post.bucket_arn
}

output "bucket_domain_name" {
  value = module.digital_bottle_post.bucket_domain_name
}
```

## Module Inputs

| Name                     | Description                                                              | Type     | Default    | Required |
| :----------------------- | :----------------------------------------------------------------------- | :------- | :--------- | :------- |
| `bucket_name_prefix`     | Prefix for the S3 bucket name. A unique suffix will be appended.         | `string` | `null`     | yes      |
| `message_retention_days` | Number of days after which messages (objects) will be expired.           | `number` | `30`       | no       |
| `enable_public_read`     | Set to `true` to allow public read access to objects in the bucket.      | `bool`   | `false`    | no       |
| `tags`                   | A map of tags to assign to the bucket.                                   | `map(string)` | `{}`      | no       |
| `versioning_enabled`     | Whether to enable versioning for the bucket.                             | `bool`   | `true`     | no       |

## Module Outputs

| Name                 | Description                                  |
| :------------------- | :------------------------------------------- |
| `bucket_id`          | The name (ID) of the S3 bucket.              |
| `bucket_arn`         | The ARN of the S3 bucket.                    |
| `bucket_domain_name` | The domain name of the S3 bucket.            |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 5.0`

## Development & Testing

To test this module locally:

1.  Navigate to the `tests/` directory.
2.  Ensure `jq` is installed (`sudo apt-get install jq` or `brew install jq`).
3.  Run `terraform init -backend=false`
4.  Execute `bash test.sh` to run the automated tests.
