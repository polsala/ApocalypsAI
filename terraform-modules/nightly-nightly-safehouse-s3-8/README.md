# Nightly Safehouse S3 Terraform Module

## Overview
Creates an Amazon S3 bucket configured for a post‑apocalyptic safehouse:

* **Versioning** – keep historical copies of objects.
* **Server‑side encryption** – AES‑256 encryption at rest.
* **Lifecycle rule** – automatically delete objects older than 30 days (ideal for perishable supplies).
* **Supply‑cache object** – a placeholder text file (`supply-cache.txt`) that can be replaced with actual inventory.

## Usage
```hcl
module "safehouse" {
  source      = "./nightly-safehouse-s3"
  bucket_name = "my‑safehouse‑bucket"
  # optional: aws_region = "us-west-2"
}

output "bucket_id"  { value = module.safehouse.bucket_id }
output "bucket_arn" { value = module.safehouse.bucket_arn }
```

## Variables
| Name | Description | Type | Default |
|------|-------------|------|---------|
| `bucket_name` | Name of the S3 bucket for the safehouse. | `string` | – |
| `aws_region`  | AWS region to create the bucket in. | `string` | `"us-east-1"` |

## Outputs
| Name | Description |
|------|-------------|
| `bucket_id`  | The ID of the created bucket. |
| `bucket_arn` | The ARN of the created bucket. |

## Testing
Run the provided test script:
```bash
cd nightly-safehouse-s3/tests
./validate.sh
```
The script checks that Terraform can initialize and validates the configuration, and also verifies that the expected resources are defined.
