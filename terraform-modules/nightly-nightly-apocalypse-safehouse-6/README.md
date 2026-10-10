# Nightly Apocalypse Safehouse Terraform Module

A whimsical yet practical Terraform module that creates a hardened S3 bucket (versioned, encrypted, with a 30‑day lifecycle) and a DynamoDB table to store supply‑cache metadata. Ideal for post‑apocalyptic projects that still need cloud storage.

## Usage

```hcl
module "safehouse" {
  source               = "git::https://github.com/yourorg/apocalypsai.git//terraform-modules/nightly-apocalypse-safehouse"
  bucket_name          = "my-safehouse-bucket"
  dynamodb_table_name  = "supply-cache"
  tags = {
    Environment = "production"
    Project     = "apocalypse"
  }
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| bucket_name | Name of the S3 bucket | string | n/a | yes |
| dynamodb_table_name | Name of the DynamoDB table | string | n/a | yes |
| tags | Tags to apply to resources | map(string) | {} | no |

## Outputs

| Name | Description |
|------|-------------|
| bucket_id | ID of the created S3 bucket |
| bucket_arn | ARN of the S3 bucket |
| dynamodb_table_name | Name of the DynamoDB table |

## Testing

Run the included test script:

```sh
cd terraform-modules/nightly-apocalypse-safehouse
./tests/test_main.sh
```

The script runs `terraform init -backend=false` and `terraform validate`. It should exit with code 0.

## License

MIT
