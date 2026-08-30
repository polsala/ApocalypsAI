# Nightly Apocalyptic Safehouse Terraform Module

## Overview

This Terraform module creates a lightweight "safe‑house" infrastructure suitable for a post‑apocalyptic scenario. It provisions:

- An S3 bucket named `<safehouse_name>-supplies` for storing essential supplies.
- A DynamoDB table `<safehouse_name>-inventory` to track inventory items.
- An IAM role with read‑only access to the bucket and table.

## Usage

```hcl
module "safehouse" {
  source         = "github.com/yourorg/apocalypsai//terraform-modules/nightly-apocalypse-safehouse"
  region         = "us-east-1"
  safehouse_name = "haven"
}
```

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| region | AWS region to deploy resources | string | n/a |
| safehouse_name | Base name for resources (must be lowercase, alphanumeric, hyphens) | string | n/a |

## Outputs

| Name | Description |
|------|-------------|
| bucket_name | Name of the S3 bucket |
| table_name | Name of the DynamoDB table |
| iam_role_arn | ARN of the IAM role |

## Testing

Run the validation script:

```sh
cd tests && ./validate.sh
```
