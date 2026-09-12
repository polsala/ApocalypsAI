# Nightly Digital Time Capsule

A Terraform module to provision a highly durable and immutable digital time capsule in AWS S3, perfect for long-term archival of digital memories, important documents, or future messages.

## 🌟 Whimsical Purpose

Ever wanted to send a message to your future self, or preserve a snapshot of today's digital world for generations to come? The Nightly Digital Time Capsule allows you to do just that! Store your most cherished (or most embarrassing) digital artifacts in a secure, immutable vault, destined to be discovered by future you, or perhaps, future sentient AIs.

## 🛠️ Technical Utility

This module creates an AWS S3 bucket configured for maximum data durability and immutability, making it ideal for long-term archival and compliance needs.

### Features:
- **Versioning Enabled**: Keeps all versions of your objects, protecting against accidental deletions or overwrites.
- **Object Lock (WORM)**: Ensures objects are immutable for a specified retention period (Governance or Compliance mode). Once locked, objects cannot be overwritten or deleted until the retention period expires.
- **Lifecycle Management**: Automatically transitions objects to AWS Glacier Deep Archive for cost-effective, ultra-long-term storage after a configurable number of days.
- **Block Public Access**: Prevents any public access to the bucket, ensuring your time capsule remains private.
- **Server-Side Encryption**: All objects are encrypted at rest using AES256.

## 🚀 Usage

To use this module, include it in your Terraform configuration:

```terraform
module "my_digital_time_capsule" {
  source = "github.com/polsala/ApocalypsAI//terraform-modules/nightly-digital-time-capsule/src" # Adjust path if cloning locally

  bucket_name           = "my-future-memories-time-capsule-2024" # Must be globally unique
  object_lock_mode      = "COMPLIANCE"                           # Or "GOVERNANCE"
  object_lock_days      = 3650                                   # 10 years of immutability
  archive_transition_days = 90                                   # Move to Deep Archive after 90 days
  tags = {
    Owner       = "ApocalypsAI"
    Project     = "TimeCapsule"
    CreationDate = "2024-07-20"
  }
}

output "time_capsule_bucket_name" {
  value       = module.my_digital_time_capsule.bucket_id
  description = "The name of the created S3 bucket."
}

output "time_capsule_bucket_arn" {
  value       = module.my_digital_time_capsule.bucket_arn
  description = "The ARN of the created S3 bucket."
}
```

### Requirements

- Terraform `v1.0+`
- AWS Provider `v4.0+`
- Configured AWS credentials (e.g., via `~/.aws/credentials` or environment variables)

## ⚙️ Inputs

| Name                    | Description                                                               | Type        | Default      | Required |
|-------------------------|---------------------------------------------------------------------------|-------------|--------------|----------|
| `bucket_name`           | The name of the S3 bucket for the time capsule.                           | `string`    | n/a          | yes      |
| `object_lock_mode`      | The object lock retention mode. Can be 'GOVERNANCE' or 'COMPLIANCE'.      | `string`    | `"GOVERNANCE"` | no       |
| `object_lock_days`      | The number of days for object lock retention.                             | `number`    | `3650` (10 years) | no       |
| `archive_transition_days` | The number of days after which objects transition to GLACIER_DEEP_ARCHIVE. | `number`    | `90`         | no       |
| `tags`                  | A map of tags to assign to the bucket.                                    | `map(string)` | `{}`         | no       |

## 💾 Outputs

| Name                     | Description                               |
|--------------------------|-------------------------------------------|
| `bucket_id`              | The ID (name) of the S3 bucket.           |
| `bucket_arn`             | The ARN of the S3 bucket.                 |

## 🧪 Testing

The module includes a self-contained test script that uses `terraform plan -json` to verify the generated infrastructure plan without deploying actual resources.

To run the tests:

```bash
cd terraform-modules/nightly-digital-time-capsule/tests
./test.sh
```

This requires `terraform` and `jq` to be installed on your system.
