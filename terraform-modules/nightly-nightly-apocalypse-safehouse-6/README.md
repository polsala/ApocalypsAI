# Apocalyptic Safehouse S3 Bucket

Creates an S3 bucket configured for post‑apocalyptic data storage with versioning, server‑side encryption, and a lifecycle rule that deletes objects older than 30 days.

## Usage

```hcl
module "safehouse" {
  source      = "./"
  bucket_name = "my-safehouse-bucket"
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| bucket_name | Name of the S3 bucket | string | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| bucket_arn | ARN of the created bucket |
| bucket_id  | ID of the bucket |

## Testing

Run `./tests/run.sh` to execute `terraform init` and `terraform validate`.
