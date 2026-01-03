# Safehouse S3 Bucket

Terraform module that creates an S3 bucket with server‑side encryption, versioning, and a lifecycle rule that expires objects after 30 days. Ideal for storing critical data in a post‑apocalyptic scenario.

## Usage

```hcl
module "safehouse_bucket" {
  source      = "./"
  bucket_name = "my-safehouse-bucket"
}
```

## Inputs

| Name            | Description                         | Type   | Default |
|-----------------|-------------------------------------|--------|---------|
| bucket_name     | Name of the S3 bucket               | string | n/a     |
| versioning      | Enable versioning                   | bool   | true    |
| expiration_days | Days after which objects are deleted| number | 30      |

## Outputs

| Name      | Description               |
|-----------|---------------------------|
| bucket_id | The ID of the created bucket |
| bucket_arn| ARN of the bucket |

## Testing

Run `tests/test.sh` to validate the module.
