# Nightly AWS Echo Chamber

A whimsical-yet-useful Terraform module to provision a "Temporal Echo Chamber" in AWS. This module sets up a serverless architecture to store and retrieve timestamped messages, or "echoes," in the cloud.

## Features

*   **Echo Storage**: Automatically stores incoming messages with a unique timestamp in an AWS S3 bucket.
*   **Echo Retrieval**: Provides an API endpoint to retrieve stored echoes, with optional filtering by timestamp prefix.
*   **Serverless**: Leverages AWS Lambda and API Gateway for a cost-effective and scalable solution.
*   **Configurable**: Easily customize resource names and AWS region.

## Architecture

The module provisions the following AWS resources:

*   **AWS S3 Bucket**: Dedicated storage for all "echoes" (messages). Each echo is stored as a text file with its timestamp as part of the key.
*   **AWS Lambda Function**: A Python-based function that acts as the core logic. It handles:
    *   `POST /echo`: Receives a message, adds a UTC timestamp, and saves it to the S3 bucket.
    *   `GET /echo`: Retrieves a list of echoes from the S3 bucket. Supports a `prefix` query parameter to filter by timestamp (e.g., `?prefix=echoes/2023-10-27`) and a `limit` parameter to control the number of returned echoes.
*   **AWS API Gateway**: Exposes the Lambda function as a RESTful API endpoint, making the Echo Chamber accessible over HTTP.
*   **AWS IAM Role and Policy**: Configures the necessary permissions for the Lambda function to interact with S3 and CloudWatch Logs.

## Usage

To deploy your own Temporal Echo Chamber, create a `main.tf` file in your Terraform project:

```terraform
provider "aws" {
  region = "us-east-1" # Or your desired AWS region
}

module "my_echo_chamber" {
  source = "./path/to/nightly-aws-echo-chamber" # Adjust this path to where you place the module
  
  project_name       = "my-apocalypsai-project"
  bucket_name_prefix = "my-unique-prefix" # Ensure this is globally unique for S3
  region             = "us-east-1"        # Must match provider region
}

output "echo_chamber_api_url" {
  description = "The URL to interact with your Echo Chamber API."
  value       = module.my_echo_chamber.api_gateway_url
}

output "echo_chamber_s3_bucket" {
  description = "The name of the S3 bucket storing your echoes."
  value       = module.my_echo_chamber.s3_bucket_name
}
```

Then, run the standard Terraform commands:

```bash
terraform init
terraform plan
terraform apply
```

After deployment, you can interact with your Echo Chamber:

*   **Submit an echo (POST request):**
    ```bash
    API_URL=$(terraform output -raw echo_chamber_api_url)
    curl -X POST -H "Content-Type: application/json" -d '{"message": "Hello from the past!"}' "$API_URL/echo"
    ```
*   **Retrieve echoes (GET request):**
    ```bash
    API_URL=$(terraform output -raw echo_chamber_api_url)
    curl "$API_URL/echo"
    # Retrieve echoes from a specific day (e.g., today)
    # curl "$API_URL/echo?prefix=echoes/$(date -u +%Y-%m-%d)"
    # Retrieve the 5 most recent echoes
    # curl "$API_URL/echo?limit=5"
    ```

## Inputs

| Name                 | Description                                                 | Type   | Default         | Required |
| :------------------- | :---------------------------------------------------------- | :----- | :-------------- | :------- |
| `region`             | AWS region to deploy resources.                             | `string` | `"us-east-1"`   | no       |
| `project_name`       | A unique name for the project, used to prefix resource names. | `string` |                 | yes      |
| `bucket_name_prefix` | A prefix for the S3 bucket name to ensure uniqueness.       | `string` | `"apocalypsai"` | no       |

## Outputs

| Name                | Description                                         |
| :------------------ | :-------------------------------------------------- |
| `api_gateway_url`   | The invoke URL of the API Gateway endpoint.         |
| `s3_bucket_name`    | The name of the S3 bucket used to store echoes.     |

## Testing

The module includes an offline test script to validate its configuration without deploying to AWS.

To run the tests:

1.  Ensure you have `terraform` and `jq` installed.
2.  Navigate to the `nightly-aws-echo-chamber` directory.
3.  Execute the test script:

    ```bash
    ./tests/test_plan.sh
    ```

This script will:
*   Create a temporary directory and copy the module's source.
*   Generate a minimal `test.tf` to instantiate the module with mock variables.
*   Run `terraform init -backend=false` to initialize without a real backend.
*   Run `terraform validate` to check for syntax errors.
*   Run `terraform plan -out=tfplan` to generate an execution plan.
*   Use `terraform show -json tfplan` and `jq` to assert that the expected AWS resources (S3 bucket, Lambda function, API Gateway) are present in the plan with the correct naming conventions.

This provides a deterministic and offline way to ensure the module's integrity.
