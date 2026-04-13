# nightly-terraform-lambda-deploy

This Terraform module simplifies deploying an AWS Lambda function by automatically provisioning required resources such as IAM roles, policies, and CloudWatch log groups.

## Features

- Creates IAM role with basic Lambda execution permissions
- Sets up CloudWatch Logs group for Lambda function
- Deploys ZIP-based Lambda functions
- Configurable timeout and memory size

## Usage

```hcl
module "lambda_function" {
  source = "./terraform-lambda-deploy"

  function_name = "my-lambda-function"
  handler       = "index.handler"
  runtime       = "nodejs18.x"
  filename      = "function.zip"
  timeout       = 30
  memory_size   = 128
}
```

## Inputs

| Name           | Description                     | Type        | Default |
|----------------|----------------------------------|-------------|---------|
| function_name  | The name of the Lambda function  | `string`    | n/a     |
| handler        | Function entry point             | `string`    | n/a     |
| runtime        | Runtime environment              | `string`    | n/a     |
| filename       | Path to deployment package       | `string`    | n/a     |
| timeout        | Timeout in seconds               | `number`    | 3       |
| memory_size    | Memory allocated in MB           | `number`    | 128     |

## Outputs

| Name         | Description                      |
|--------------|-----------------------------------|
| function_arn | ARN of the created Lambda function|
