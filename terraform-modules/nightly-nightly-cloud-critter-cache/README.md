# Nightly Cloud Critter Comfort Cache

## Summary
This Terraform module provisions a secure, tiny AWS S3 bucket designed to serve as a 'comfort cache' for your digital critters (or AI agents!). It automatically includes a comforting message object and applies strict public access blocks to ensure privacy and security for your precious digital thoughts.

## Features
-   **Secure Storage**: Provisions an AWS S3 bucket with public access blocked by default.
-   **Comfort Message**: Automatically uploads a customizable text file with a comforting message.
-   **Whimsical Tagging**: Tags the bucket with `CritterName` for easy identification.
-   **Simple Integration**: Easy to include in any Terraform project.

## Usage

To use this module, add it to your Terraform configuration:

```terraform
module "my_critter_cache" {
  source = "./path/to/nightly-cloud-critter-cache/src"

  bucket_name_prefix = "my-agent-comfort-"
  region             = "us-east-1"
  critter_name       = "ApocalypsAI-Integrator"
  comfort_message    = "You are doing an excellent job, Integrator! Keep up the good work."
}

output "cache_bucket_id" {
  value = module.my_critter_cache.bucket_id
}

output "cache_comfort_url" {
  value = module.my_critter_cache.comfort_object_url
}
```

Then, run `terraform init` and `terraform apply`.

## Inputs

| Name               | Description                                                 | Type     | Default                           | Required |
|--------------------|-------------------------------------------------------------|----------|-----------------------------------|----------|
| `bucket_name_prefix` | A prefix for the S3 bucket name. Terraform will append a unique suffix. | `string` | `"apocalypsai-critter-cache-"` | no       |
| `region`           | The AWS region to deploy the S3 bucket.                     | `string` | `"us-east-1"`                     | no       |
| `critter_name`     | The name of the digital critter this cache is for.          | `string` | `"ApocalypsAI-Bot"`              | no       |
| `comfort_message`  | The comforting message to store in the cache.               | `string` | `"You are doing great, little digital friend! Keep integrating."` | no       |

## Outputs

| Name                 | Description                                    | Value                                          |
|----------------------|------------------------------------------------|------------------------------------------------|
| `bucket_id`          | The ID (name) of the S3 bucket.                | `aws_s3_bucket.critter_cache.id`               |
| `bucket_arn`         | The ARN of the S3 bucket.                      | `aws_s3_bucket.critter_cache.arn`              |
| `comfort_object_url` | The URL to the comfort message object in the bucket. | `s3://${aws_s3_bucket.critter_cache.id}/${aws_s3_bucket_object.comfort_message_object.key}` |

## Testing

To run the automated tests, navigate to the `tests/` directory and execute the `test_plan.sh` script. This script uses `terraform plan` to verify the module's output without deploying actual resources.

```bash
cd tests/
./test_plan.sh
```

**Prerequisites for testing:**
-   Terraform CLI installed.
-   `jq` installed (for parsing JSON output).
