# Nightly Safehouse S3 Terraform Module

A whimsical Terraform module that creates a version‑enabled S3 bucket for storing post‑apocalyptic supplies. The bucket name is prefixed by a user‑provided string and suffixed with a random ID to avoid collisions. Includes a lifecycle rule that expires objects after 30 days.

## Usage

```hcl
module "safehouse_s3" {
  source             = "github.com/yourorg/polsala/terraform-modules/nightly-safehouse-s3"
  bucket_name_prefix = "my-safehouse"
  tags = {
    Environment = "apocalypse"
    Owner       = "survivor"
  }
}
```

Run:

```sh
terraform init
terraform apply
```

## Inputs

- `bucket_name_prefix` (string, required): Prefix for the bucket name.
- `tags` (map(string), optional): Tags to apply to the bucket.
- `aws_region` (string, optional): AWS region (default `us-east-1`).

## Outputs

- `bucket_id` – The name of the bucket.
- `bucket_arn` – The ARN of the bucket.

## Testing

```sh
cd tests && ./test_main.sh
```
