# Nightly Wasteland Safehouse S3

A whimsical Terraform module that creates a secure, versioned S3 bucket for storing your post‑apocalyptic data. The bucket has server‑side encryption, versioning, and a lifecycle rule that transitions objects to Glacier after 30 days and expires after 365 days.

## Usage

```hcl
module "safehouse" {
  source = "github.com/yourorg/polsala/ApocalypsAI//terraform-modules/nightly-wasteland-safehouse-s3"

  bucket_name = "my‑post‑apoc‑vault"
  tags        = {
    Environment = "Wasteland"
    Owner       = "Survivor"
  }
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| bucket_name | Name of the S3 bucket (must be globally unique) | string | n/a | yes |
| tags | A map of tags to assign to the bucket | map(string) | {} | no |

## Outputs

| Name | Description |
|------|-------------|
| bucket_id | The ID of the created bucket |
| bucket_arn | The ARN of the created bucket |

## Testing

Run the provided test script:

```sh
cd tests && ./validate.sh
```

It will initialize the module and run `terraform validate` (mocked for offline CI).
