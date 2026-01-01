# nightly-terraform-quickstart-s3

A minimal Terraform module that provisions an S3 bucket with versioning and lifecycle rules.

## Usage

```hcl
module "s3_bucket" {
  source = "./nightly-terraform-quickstart-s3"

  bucket_name = "my-unique-bucket"
}
```

## Variables

- `bucket_name` (string, required): The name of the S3 bucket.

## Outputs

- `bucket_id` (string): The ID of the created bucket.

## License

MIT
