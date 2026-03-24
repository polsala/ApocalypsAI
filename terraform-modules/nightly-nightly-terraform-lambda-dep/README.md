# nightly-terraform-lambda-deploy

A Terraform module for deploying AWS Lambda functions with automatic ZIP packaging and IAM role provisioning.

## Features

- Automatic creation of IAM execution role with basic Lambda permissions
- ZIP packaging of source code
- Deployment of Lambda function with configurable memory, timeout, and environment variables

## Usage

```hcl
module "lambda_function" {
  source = "./terraform-lambda-deploy"

  function_name = "my-function"
  handler       = "index.handler"
  runtime       = "nodejs18.x"
  source_dir    = "${path.module}/lambda-src"

  environment_variables = {
    ENV = "prod"
  }
}
```

## Inputs

| Name                  | Description                        | Type     | Default |
|-----------------------|------------------------------------|----------|---------|
| function_name         | The name of the Lambda function    | string   | n/a     |
| handler               | Function entrypoint                | string   | n/a     |
| runtime               | Runtime identifier                 | string   | n/a     |
| source_dir            | Path to function source code       | string   | n/a     |
| memory_size           | Memory in MB                       | number   | 128     |
| timeout               | Timeout in seconds                 | number   | 30      |
| environment_variables | Environment variables map          | map(any) | {}      |

## Outputs

| Name         | Description             |
|--------------|-------------------------|
| function_arn | ARN of created function |
