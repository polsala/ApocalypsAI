# Apocalyptic Safehouse S3 Terraform Module

This module creates an AWS S3 bucket configured for versioning and a lifecycle rule that transitions objects to Glacier after 30 days and expires them after 365 days—perfect for storing post‑apocalyptic data.

## Usage

```hcl
module "safehouse" {
  source      = "github.com/yourorg/apocalypsai//terraform-modules/nightly-apocalypse-safeguard-s3"
  bucket_name = "my‑post‑apoc‑store"
}
```

## Inputs

| Name        | Description               | Type   | Required |
|-------------|---------------------------|--------|----------|
| bucket_name | Name of the S3 bucket     | string | yes      |

## Outputs

| Name       | Description                     |
|------------|---------------------------------|
| bucket_arn | ARN of the created bucket       |

## Testing

Run the provided test script:

```sh
cd test
./test_module.sh
```
