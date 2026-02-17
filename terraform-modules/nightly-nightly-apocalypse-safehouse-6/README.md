# Nightly Apocalypse Safehouse S3 Terraform Module

This Terraform module creates an Amazon S3 bucket configured as a post‑apocalyptic safe‑house storage. Features:

* Versioning enabled – keep every revision of your precious supplies.
* Lifecycle rule that transitions objects to Glacier after 30 days and permanently deletes them after 365 days.
* Optional server‑side encryption with AWS‑managed keys.
* Bucket name is fully customizable.

## Usage

```hcl
module "safehouse" {
  source            = "git::https://github.com/yourorg/polsala.git//terraform-modules/nightly-apocalypse-safehouse-s3"
  bucket_name       = "my-apocalypse-stash"
  enable_encryption = true
}
```

## Inputs

| Name               | Description                                      | Type   | Default |
|--------------------|--------------------------------------------------|--------|---------|
| bucket_name        | Name of the S3 bucket                            | string | n/a     |
| enable_encryption  | Whether to enable SSE‑S3 encryption              | bool   | false   |
| transition_days    | Days after which objects transition to Glacier   | number | 30      |
| expiration_days    | Days after which objects are deleted permanently | number | 365     |

## Outputs

| Name      | Description               |
|-----------|---------------------------|
| bucket_id | The ID of the created bucket |
| bucket_arn| ARN of the bucket |
