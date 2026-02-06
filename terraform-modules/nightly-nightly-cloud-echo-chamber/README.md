# Nightly Cloud Echo Chamber

This Terraform module provisions a secure AWS S3 bucket, acting as a "Cloud Echo Chamber," designed to store data securely while providing robust observability. It includes server access logging to a dedicated bucket and can optionally deploy an AWS Lambda function to "echo" object creation events (metadata only) to CloudWatch Logs, ensuring every whisper in the chamber resonates for analysis.

## Features

*   **Secure S3 Storage**: Private bucket with server-side encryption (SSE-S3) and versioning enabled.
*   **Access Logging**: Configures server access logging to a separate, dedicated S3 bucket.
*   **Optional Lambda Echo**: Deploys an AWS Lambda function triggered by new object creation, logging object metadata (bucket, key, size, ETag) to CloudWatch Logs.
*   **IAM Best Practices**: Least privilege IAM roles for the Lambda function.
*   **Tagging**: Supports custom tags for resource organization.

## Usage

To use this module, define it in your Terraform configuration:

```terraform
module "echo_chamber" {
  source = "./src" # Or a Git/Terraform Registry source
  
  region               = "us-east-1"
  bucket_name_prefix   = "my-apocalypsai-echo"
  enable_lambda_echo   = true
  tags = {
    Project     = "ApocalypsAI"
    Environment = "Dev"
  }
}

output "echo_chamber_bucket_id" {
  description = "The ID of the main S3 Echo Chamber bucket."
  value       = module.echo_chamber.echo_chamber_bucket_id
}

output "lambda_function_arn" {
  description = "The ARN of the Lambda Echo function (if enabled)."
  value       = module.echo_chamber.lambda_function_arn
}
```

## Inputs

| Name                 | Description                                                               | Type          | Default   | Required |
| :------------------- | :------------------------------------------------------------------------ | :------------ | :-------- | :------- |
| `region`             | AWS region to deploy resources into.                                      | `string`      | n/a       | yes      |
| `bucket_name_prefix` | A unique prefix for the S3 bucket names.                                  | `string`      | n/a       | yes      |
| `enable_lambda_echo` | Whether to deploy the Lambda function to echo object metadata to CloudWatch Logs. | `bool`        | `true`    | no       |
| `tags`               | A map of tags to apply to all resources.                                  | `map(string)` | `{}`      | no       |

## Outputs

| Name                        | Description                                     |
| :-------------------------- | :---------------------------------------------- |
| `echo_chamber_bucket_id`    | The ID of the main S3 Echo Chamber bucket.     |
| `echo_chamber_bucket_arn`   | The ARN of the main S3 Echo Chamber bucket.    |
| `logging_bucket_id`         | The ID of the S3 bucket storing access logs.    |
| `logging_bucket_arn`        | The ARN of the S3 bucket storing access logs.   |
| `lambda_function_arn`       | The ARN of the Lambda Echo function (if enabled). |
| `cloudwatch_log_group_name` | The name of the CloudWatch Log Group for Lambda (if enabled). |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 5.0`

## Testing

This module includes a basic `test.sh` script that performs `terraform validate` to ensure the module's syntax and configuration are correct without deploying actual resources.

```bash
cd tests
./test.sh
```
