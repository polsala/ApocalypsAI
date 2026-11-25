# Nightly Temporal Outpost Deployer

This Terraform module deploys a whimsical, serverless 'Temporal Anomaly Detection Outpost' to AWS. Its purpose is to periodically 'scan' the time-space continuum and log its 'temporal signature' (or detected anomalies) to an S3 bucket.

While playfully themed, this utility demonstrates a practical serverless pattern: a scheduled AWS Lambda function writing logs to an S3 bucket, managed entirely with Infrastructure-as-Code.

## Features

-   **Serverless Architecture**: Utilizes AWS Lambda, S3, and EventBridge (CloudWatch Events) for cost-effective and scalable operation.
-   **Scheduled Scans**: The Lambda function runs on a configurable schedule (e.g., every 5 minutes, daily).
-   **Whimsical Anomaly Detection**: The Lambda function randomly reports stable signatures, minor ripples, or major temporal anomalies.
-   **Centralized Logging**: All temporal signatures are stored as JSON files in a dedicated S3 bucket.
-   **Infrastructure-as-Code**: Fully defined and deployed using Terraform.

## Prerequisites

-   [Terraform](https://www.terraform.io/downloads.html) installed.
-   AWS CLI configured with credentials that have permissions to create S3 buckets, Lambda functions, IAM roles/policies, and EventBridge rules.

## Usage

1.  **Create a `main.tf` file** in a new directory (e.g., `my-outpost-deployment`):

    ```terraform
    module "temporal_outpost" {
      source = "./path/to/nightly-temporal-outpost-deployer/src"

      # Required variables
      aws_region          = "us-east-1" # Or your desired AWS region
      bucket_name         = "my-unique-temporal-logs-bucket-12345" # MUST be globally unique
      schedule_expression = "rate(15 minutes)" # e.g., "rate(5 minutes)" or "cron(0 10 * * ? *)"

      # Optional variables (defaults are provided)
      name_prefix = "apocalypsai-outpost"
      environment = "prod"
    }

    output "s3_bucket_name" {
      value = module.temporal_outpost.s3_bucket_name
    }

    output "lambda_function_name" {
      value = module.temporal_outpost.lambda_function_name
    }
    ```

    *Replace `./path/to/nightly-temporal-outpost-deployer/src` with the actual path to the `src` directory of this module.*

2.  **Initialize Terraform**:

    ```bash
    terraform init
    ```

3.  **Review the plan**:

    ```bash
    terraform plan
    ```

4.  **Apply the configuration**:

    ```bash
    terraform apply
    ```

    Confirm with `yes` when prompted.

## After Deployment

-   The Lambda function will start executing according to your `schedule_expression`.
-   Logs will appear in the specified S3 bucket under `temporal-logs/YYYY-MM-DD/`.
-   You can monitor the Lambda function's invocations and logs in AWS CloudWatch.

## Cleanup

To destroy all resources created by this module:

```bash
terraform destroy
```

Confirm with `yes` when prompted.
