# Nightly Ephemeral Message Beacon

This Terraform module provisions a highly ephemeral, low-cost cloud storage bucket (specifically AWS S3) designed to host a single, short-lived "message of hope" or "critical instruction". It automatically configures lifecycle rules to delete objects within the bucket after a configurable duration, ensuring your fleeting messages truly vanish into the digital ether.

## Whimsical Purpose

In the chaotic post-apocalyptic landscape, sometimes you just need to leave a quick, vital note for a fellow survivor, knowing it will self-destruct after it's been seen (or if it hasn't). This beacon is your digital dead drop, a whisper in the cloud that fades with the dawn.

## Features

*   **Ephemeral Storage**: Objects are automatically deleted after a specified number of days.
*   **Secure by Default**: Bucket is private, blocking public access. You manage object-level access (e.g., via pre-signed URLs) after provisioning.
*   **Region Agnostic**: Deployable in any AWS region.
*   **Low Cost**: Utilizes S3 Standard storage, with lifecycle rules to minimize long-term costs.

## Usage

To use this module, include it in your Terraform configuration:

```terraform
module "message_beacon" {
  source = "./path/to/nightly-ephemeral-message-beacon/src"

  bucket_prefix   = "my-secret-beacon"
  expiration_days = 3
  aws_region      = "us-east-1"
}

output "beacon_url" {
  description = "The domain name of the ephemeral message beacon bucket."
  value       = module.message_beacon.bucket_domain_name
}

output "beacon_name" {
  description = "The name of the ephemeral message beacon bucket."
  value       = module.message_beacon.bucket_id
}
```

### Inputs

| Name              | Description                                                              | Type   | Default             | Required |
| :---------------- | :----------------------------------------------------------------------- | :----- | :------------------ | :------- |
| `bucket_prefix`   | A prefix for the S3 bucket name. The full name will be `prefix-randomstring`. | `string` | `apocalypsai-beacon` | no       |
| `expiration_days` | Number of days after which objects in the bucket will be automatically deleted. | `number` | `7`                 | no       |
| `aws_region`      | The AWS region where the S3 bucket will be created.                      | `string` | `us-east-1`         | no       |

### Outputs

| Name                 | Description                                    |
| :------------------- | :--------------------------------------------- |
| `bucket_id`          | The ID (name) of the created S3 bucket.        |
| `bucket_arn`         | The ARN of the created S3 bucket.              |
| `bucket_domain_name` | The domain name of the created S3 bucket.      |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 4.0`
*   Configured AWS credentials (e.g., via `~/.aws/credentials` or environment variables).

## Contributing

Feel free to suggest improvements or new features! This beacon is for everyone.
