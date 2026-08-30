# Nightly Digital Doomsday Bunker

A Terraform module to provision a highly available, cost-optimized digital bunker for critical post-apocalyptic data storage using AWS S3. This module sets up an S3 bucket with versioning, server-side encryption, and lifecycle rules to ensure your vital data (e.g., survival guides, seed bank manifests, cat memes) is safe and sound, even when the world goes sideways.

## Features

*   **Highly Available**: Leverages AWS S3's inherent durability across multiple availability zones.
*   **Data Protection**: Configures S3 versioning to protect against accidental deletions and overwrites.
*   **Encryption at Rest**: Uses S3 Server-Side Encryption (SSE-S3) by default.
*   **Cost Optimization**: Includes a lifecycle rule to transition older, non-current versions to S3 Glacier Deep Archive after a configurable number of days, and expire them after a configurable number of days, reducing long-term storage costs.
*   **Secure by Default**: Blocks public access and sets private ACL.

## Usage

To use this module, include it in your Terraform configuration:

```terraform
module "doomsday_bunker" {
  source = "./src" # Or a remote source like "github.com/polsala/ApocalypsAI//terraform-modules/nightly-digital-doomsday-bunker/src?ref=main"

  bucket_name_prefix = "my-apocalypse-data"
  region             = "us-east-1"
  tags = {
    Project     = "ApocalypsAI"
    Environment = "Production"
    Purpose     = "DoomsdayBunker"
  }
  glacier_transition_days = 45
  glacier_expiration_days = 400
}

output "bunker_bucket_id" {
  value       = module.doomsday_bunker.bucket_id
  description = "The ID of the Digital Doomsday Bunker S3 bucket."
}

output "bunker_bucket_arn" {
  value       = module.doomsday_bunker.bucket_arn
  description = "The ARN of the Digital Doomsday Bunker S3 bucket."
}
```

## Inputs

| Name                      | Description                                                                 | Type     | Default                     | Required |
| :------------------------ | :-------------------------------------------------------------------------- | :------- | :-------------------------- | :------- |
| `bucket_name_prefix`      | A prefix for the S3 bucket name. A unique suffix will be appended.          | `string` | `"apocalypsai-bunker"`     | no       |
| `region`                  | The AWS region where the S3 bucket will be created.                         | `string` | `"us-east-1"`               | no       |
| `tags`                    | A map of tags to assign to the S3 bucket.                                   | `map`    | `{}`                        | no       |
| `glacier_transition_days` | Number of days after which non-current versions transition to Glacier Deep Archive. | `number` | `30`                        | no       |
| `glacier_expiration_days` | Number of days after which non-current versions expire from Glacier Deep Archive. | `number` | `365`                       | no       |

## Outputs

| Name                 | Description                                     |
| :------------------- | :---------------------------------------------- |
| `bucket_id`          | The ID of the S3 bucket.                        |
| `bucket_arn`         | The ARN of the S3 bucket.                       |
| `bucket_domain_name` | The domain name of the S3 bucket.               |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 5.0`
*   Random Provider `~> 3.0`

## Development & Testing

This module includes a basic test setup using `terraform validate` and `terraform fmt -check`.

To run tests:

```bash
cd tests
./run_tests.sh
```
