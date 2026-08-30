# Nightly Temporal Echo Chamber

This Terraform module provisions an AWS S3 bucket designed to serve as a temporary "echo chamber" for community messages, logs, or ephemeral data. It's configured with a lifecycle rule to automatically expire objects after a specified number of days, ensuring that echoes fade gracefully into the digital void.

While the bucket's public access block is configured to *allow* public access (should you choose to apply a bucket policy for it), it does not inherently make the bucket or its contents public. It merely sets the stage for an open "echo chamber" if desired.

## Usage

To deploy your own Temporal Echo Chamber, include this module in your Terraform configuration:

```terraform
module "echo_chamber" {
  source = "./nightly-temporal-echo-chamber" # Adjust path if used as a local module
  # For a remote module, use:
  # source = "polsala/ApocalypsAI//terraform-modules/nightly-temporal-echo-chamber"

  bucket_name_prefix = "apocalypsai-echo-chamber"
  retention_days     = 7
  environment        = "community-dev"
}

output "echo_chamber_bucket_id" {
  value = module.echo_chamber.bucket_id
}

output "echo_chamber_bucket_arn" {
  value = module.echo_chamber.bucket_arn
}

output "echo_chamber_bucket_regional_domain_name" {
  value = module.echo_chamber.bucket_regional_domain_name
}
```

Run `terraform init`, `terraform plan`, and `terraform apply` to provision the bucket.

## Inputs

| Name                 | Description                                                               | Type   | Default       | Required |
|----------------------|---------------------------------------------------------------------------|--------|---------------|----------|
| `bucket_name_prefix` | A unique prefix for the S3 bucket name. A random suffix will be added.    | `string` | `null`        | yes      |
| `retention_days`     | Number of days after which objects in the bucket will be automatically expired. | `number` | `7`           | no       |
| `environment`        | Environment tag for the bucket.                                           | `string` | `"development"` | no       |

## Outputs

| Name                               | Description                               |
|------------------------------------|-------------------------------------------|
| `bucket_id`                        | The ID of the S3 bucket.                  |
| `bucket_arn`                       | The ARN of the S3 bucket.                 |
| `bucket_regional_domain_name`      | The regional domain name of the S3 bucket.|

## Testing

The module includes a `tests/` directory with a `main.tf` that calls the module and a `test.sh` script. The `test.sh` script performs an offline `terraform plan` and asserts expected configurations using `terraform show -json` and `jq`. This ensures the module's syntax and planned resource attributes are correct without requiring AWS credentials or actual resource deployment.
