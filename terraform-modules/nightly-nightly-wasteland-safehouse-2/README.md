# Nightly Wasteland Safehouse S3

## Overview

Terraform module that creates an S3 bucket configured as a post‑apocalyptic safe‑house: versioning enabled, server‑side encryption, a lifecycle rule that expires objects after 30 days, and an initial "supply‑cache.txt" object containing a whimsical message.

## Usage

```hcl
module "safehouse" {
  source      = "./"
  bucket_name = "my-safe-house"
}
```

## Inputs

- `bucket_name` (string, required): Name of the S3 bucket.
- `region` (string, optional, default "us-east-1"): AWS region.

## Outputs

- `bucket_id`: The ID of the created bucket.
- `supply_object_key`: Key of the initial supply cache object.

## Testing

Run the provided test script:

```sh
cd tests && ./test_module.sh
```
