# Safehouse S3 Bucket

Utility creates an S3 bucket configured for postâapocalyptic safeâhouse data storage. Features:
- Versioning
- Serverâside encryption (AESâ256)
- Lifecycle rule to expire objects after 30 days
- Publicâaccess block

## Usage

```bash
cd utils/nightly-safehouse-s3-bucket
terraform init -backend=false
terraform apply -var 'bucket_name=my-safehouse-bucket' -auto-approve
```

The module uses dummy AWS credentials by default, making it safe to run in a local test environment.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| `bucket_name` | Name of the S3 bucket. | string | â |
| `aws_region` | AWS region. | string | `us-east-1` |
| `aws_access_key` | AWS access key (dummy for testing). | string | `FAKEACCESSKEY` |
| `aws_secret_key` | AWS secret key (dummy for testing). | string | `FAKESECRETKEY` |
| `environment` | Environment tag. | string | `dev` |

## Outputs

- `bucket_id` â The ID of the created bucket.
- `bucket_arn` â The ARN of the bucket.

## Testing

Run the provided test script to ensure the configuration validates and a plan can be generated without contacting AWS:

```bash
cd tests
./test_plan.sh
```
