# nightly‑postapoc‑s3‑safehouse

A tiny Terraform module that creates an Amazon S3 bucket configured for a post‑apocalyptic safe‑house:

* **Versioning** enabled – never lose a file.
* **Lifecycle** rule: transition objects to Glacier after 30 days, delete after 365 days.
* **Customizable** bucket name and tags.

## Usage
```hcl
module "safehouse" {
  source      = "./utils/nightly-postapoc-s3-safehouse"
  bucket_name = "my‑postapoc‑vault"
  tags = {
    Environment = "production"
    Owner       = "survivors"
  }
}
```

## Inputs
| Name | Description | Type | Required |
|------|-------------|------|----------|
| `bucket_name` | Name of the S3 bucket (must be globally unique) | `string` | yes |
| `tags` | Map of tags to apply to the bucket | `map(string)` | no |

## Outputs
| Name | Description |
|------|-------------|
| `bucket_id` | The bucket's ID |
| `bucket_arn` | The bucket's ARN |

## Testing
A simple offline test script is provided under `tests/verify.sh`. It checks that the module files contain the expected resources and that `terraform fmt -check` passes.
