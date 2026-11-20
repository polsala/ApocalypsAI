# Nightly Wasteland Safehouse S3

## Overview

Terraform module that creates an S3 bucket with server‑side encryption, versioning, and a lifecycle rule that expires objects after 30 days. The bucket name is generated using the `random_pet` resource to give each safe‑house a unique, whimsical name.

## Usage

```hcl
module "safehouse" {
  source = "./"
  region = "us-east-1"
}
```

## Inputs

- `region` (string, required): AWS region.
- `bucket_prefix` (string, optional): Prefix for bucket name, default `"safehouse"`.

## Outputs

- `bucket_name` – The name of the created S3 bucket.

## Testing

Run the provided test script:

```sh
cd tests && ./test_module.sh
```
