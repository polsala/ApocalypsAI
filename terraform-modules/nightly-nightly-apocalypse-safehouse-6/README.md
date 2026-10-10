# Apocalyptic Safehouse S3 Terraform Module

## Overview
This Terraform module creates an Amazon S3 bucket configured for secure, versioned storage with server-side encryption and a lifecycle rule that automatically deletes objects older than 30 days. Ideal for storing critical data in a post-apocalyptic scenario.

## Usage
```hcl
module "safehouse" {
  source      = "./"
  bucket_name = "my-post-apoc-bucket"
  tags = {
    Environment = "production"
    Project     = "safehouse"
  }
}
```

## Variables
- `bucket_name` (string, required): Name of the bucket.
- `tags` (map(string), optional): Tags to apply.

## Outputs
- `bucket_id` – The bucket name.
- `bucket_arn` – The bucket ARN.

## Testing
Run the provided test script:
```sh
cd <module-dir>
chmod +x tests/test_module.sh
./tests/test_module.sh
```
The script runs `terraform init`, `validate`, and a dry-run `plan`. It should exit with status 0.
