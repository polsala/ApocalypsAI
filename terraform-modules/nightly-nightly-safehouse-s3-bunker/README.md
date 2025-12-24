# Nightly Safehouse S3 Bunker

A whimsical Terraform module that provisions an S3 bucket styled as a post‑apocalyptic safe‑house. The bucket has versioning, server‑side encryption, and a lifecycle rule that automatically deletes objects older than 30 days, ensuring your supplies don’t rot.

## Usage

```hcl
module "safehouse" {
  source = "./src"

  bucket_name = "my-post-apoc-supplies"
}
```

Run `terraform init` and `terraform apply`.

## Inputs

- `bucket_name` (string, required): Name of the S3 bucket.
- `aws_region` (string, optional): AWS region (default: `us-east-1`).

## Outputs

- `bucket_arn`: ARN of the created bucket.

## Testing

```sh
cd tests && ./validate.sh
```

The test runs `terraform init`, `terraform validate`, and a dry‑run `terraform plan` using a mock AWS provider configuration that skips credential checks, so it works offline.
