# Nightly Whispering Postbox

Provisions a secure, ephemeral AWS S3 bucket designed for anonymous message drops, acting as a digital dead drop in the cloud.

## Overview

The `nightly-whispering-postbox` module creates an AWS S3 bucket with a restrictive bucket policy. It's configured to allow `s3:PutObject` actions (for dropping messages) from a specified list of IP CIDR blocks, while blocking public access by default. This creates a simple, secure, and ephemeral "postbox" for one-way message delivery in the digital wasteland.

## Usage

To use this module, include it in your Terraform configuration and provide the necessary variables.

```terraform
module "whispering_postbox" {
  source = "./src" # Or "polsala/apocalypsai/nightly-whispering-postbox" in a real registry

  bucket_name_prefix = "my-secret-drop"
  allowed_ip_cidrs   = ["203.0.113.0/24", "198.51.100.0/24"] # Replace with your actual IP ranges
  region             = "us-west-2"
}

output "postbox_bucket_id" {
  value = module.whispering_postbox.bucket_id
}

output "postbox_bucket_arn" {
  value = module.whispering_postbox.bucket_arn
}
```

### Requirements

-   Terraform CLI (v1.0.0+)
-   AWS Provider configured with appropriate credentials.

## Inputs

| Name                 | Description                                                                 | Type          | Default           | Required |
| :------------------- | :-------------------------------------------------------------------------- | :------------ | :---------------- | :------- |
| `bucket_name_prefix` | A prefix for the S3 bucket name. The full name will include a random suffix. | `string`      | `"nightly-postbox"` | no       |
| `allowed_ip_cidrs`   | A list of IP CIDR blocks allowed to put objects into the bucket.            | `list(string)` | `["0.0.0.0/0"]`   | no       |
| `region`             | The AWS region where the S3 bucket will be created.                         | `string`      | `"us-east-1"`     | no       |

## Outputs

| Name             | Description               |
| :--------------- | :------------------------ |
| `bucket_id`      | The ID of the S3 bucket.  |
| `bucket_arn`     | The ARN of the S3 bucket. |

## Testing

The module includes a basic test configuration that validates the Terraform syntax and ensures a plan can be generated without errors.

To run tests:

```bash
cd tests
terraform init -backend=false
terraform validate
terraform plan -destroy -out=tfplan # Ensures a destroy plan can be generated
```
