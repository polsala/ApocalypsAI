# Safehouse S3 Bucket

This Terraform module creates an Amazon S3 bucket configured for versioning and a lifecycle rule that expires objects after 365 days. Ideal for storing critical post-apocalyptic data backups.

## Usage
```hcl
module "safehouse" {
  source      = "./"
  bucket_name = "my-safehouse-bucket"
  tags = {
    Environment = "production"
    Project     = "safehouse"
  }
}
```

## Variables
- `bucket_name` (string, required): Name of the S3 bucket.
- `tags` (map(string), optional): Tags to apply to the bucket.

## Outputs
- `bucket_id` – The ID of the created bucket.
- `bucket_arn` – The ARN of the created bucket.

## Testing
Run the provided test script:
```sh
cd tests && ./test_main.sh
```
The script runs `terraform init` and `terraform validate` locally.
