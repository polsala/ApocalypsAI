# Safehouse S3 Module

A whimsical Terraform module that creates an S3 bucket named for a safehouse, with versioning enabled and a lifecycle rule that transitions objects to Glacier after 30 days and expires after 365 days. Useful for storing emergency supplies data.

## Usage

```hcl
module "safehouse_s3" {
  source      = "./"
  bucket_name = "my-safehouse-bucket"
  region      = "us-east-1"
}
```

## Inputs

| Name        | Description          | Type   | Default |
|-------------|----------------------|--------|---------|
| bucket_name | Name of the S3 bucket| string | n/a     |
| region      | AWS region           | string | "us-east-1" |

## Outputs

| Name      | Description               |
|-----------|---------------------------|
| bucket_id | The ID of the created bucket |
| bucket_arn| The ARN of the bucket |

## Testing

Run `./tests/run_test.sh` to validate the module offline.
