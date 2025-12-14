# nightly-terraform-s3-bucket

A whimsical Terraform module that creates an S3 bucket with versioning and lifecycle rules.

## Usage

```hcl
module "my_bucket" {
  source = "../terraform-modules/nightly-terraform-s3-bucket"

  bucket_name = "my-unique-bucket"
  enable_versioning = true

  lifecycle_rules = [
    {
      prefix          = "logs/"
      enabled         = true
      expiration_days = 30
    }
  ]
}
```

## Features

- Creates an S3 bucket with the specified name.
- Enables versioning by default.
- Allows custom lifecycle rules.

## License

MIT
