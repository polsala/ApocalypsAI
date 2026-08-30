# nightly-postapoc-s3-safehouse

Creates an S3 bucket configured as a post‑apocalyptic safe‑house: versioning enabled, server‑side encryption with AES‑256, and a lifecycle rule that expires objects after 30 days. The module is provider‑agnostic; it uses the AWS provider but can be run with a mock or LocalStack for testing.

## Usage

```hcl
module "safehouse" {
  source = "github.com/yourorg/polsala//terraform-modules/nightly-postapoc-s3-safehouse"

  bucket_name = "my-safe-house-bucket"
}
```

## Inputs

- `bucket_name` (string, required): Name of the S3 bucket.

## Outputs

- `bucket_arn` – ARN of the created bucket.
- `bucket_id` – ID of the bucket.

## Testing

Run the test script:

```sh
cd tests
./validate.sh
```
