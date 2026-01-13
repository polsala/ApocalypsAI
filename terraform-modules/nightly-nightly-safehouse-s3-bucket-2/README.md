# Nightly Safehouse S3 Bucket

A whimsical yet practical Terraform module that creates an AWS S3 bucket configured for
maximum resilience in a postâapocalyptic setting. Features include:

- **Versioning** â keep every revision of your critical files.
- **ServerâSide Encryption (SSEâS3)** â data is encrypted at rest.
- **Lifecycle rule** â automatically delete objects older than 30 days to free space.

## Usage

```hcl
module "safehouse" {
  source      = "./nightly-safehouse-s3-bucket"
  bucket_name = "myâpostâapocâsafehouse"
}
```

## Variables

| Name | Description | Type | Required |
|------|-------------|------|----------|
| `bucket_name` | Name of the S3 bucket to create. Must be globally unique. | `string` | yes |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_arn` | ARN of the created S3 bucket. |

## Testing

Run the provided test script to ensure the module validates correctly without contacting AWS:

```bash
cd nightly-safehouse-s3-bucket
./tests/test_safehouse.sh
```

The test runs `terraform init -backend=false` and `terraform validate` in a sandboxed environment.

---

*Created by the ApocalypsAI Nightly Integrator.*
