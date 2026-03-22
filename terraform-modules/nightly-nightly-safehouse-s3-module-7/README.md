# Safehouse S3 Terraform Module

## Overview

Creates an S3 bucket named `<bucket_name>-safehouse` with server‑side encryption, versioning, and a lifecycle rule that deletes objects older than 30 days. It also adds an initial placeholder object `supplies.txt` containing a whimsical message.

## Usage

```hcl
module "safehouse" {
  source      = "./"
  bucket_name = "my-apocalypse"
  tags = {
    Environment = "post-apocalypse"
  }
}
```

## Inputs

| Name | Type | Description | Required |
|------|------|-------------|----------|
| `bucket_name` | `string` | Base name for the bucket. | yes |
| `tags` | `map(string)` | Tags to apply to the bucket. | no |
| `aws_region` | `string` | AWS region (defaults to `us-east-1`). | no |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_id` | ID of the created bucket |
| `bucket_arn` | ARN of the created bucket |

## Testing

Run the test script to validate the module without applying any resources:

```bash
./tests/run_test.sh
```
