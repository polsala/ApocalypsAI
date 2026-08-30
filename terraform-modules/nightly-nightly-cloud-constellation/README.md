# Nightly Cloud Constellation Mapper

This Terraform module provisions the necessary AWS infrastructure for a serverless "Cloud Constellation Mapper". This whimsical-yet-useful utility is designed to help you visualize and understand your cloud resources by categorizing them into "constellations" based on their tags.

## 🌌 What it does

The Cloud Constellation Mapper deploys an AWS Lambda function that periodically scans your AWS environment (e.g., EC2 instances, S3 buckets, RDS databases). It reads their tags (e.g., `Project`, `Environment`, `Owner`) and groups them into logical "constellations".

It also helps identify:
-   **Rogue Stars**: Resources that are untagged or missing critical tags.
-   **Cosmic Dust**: Potentially underutilized or orphaned resources (though the current Lambda provides a basic framework, advanced detection would require further logic).

The output of the mapping process (a JSON file) is stored in a dedicated S3 bucket, ready for further processing or visualization by other tools.

## ✨ Features

-   **Automated Scanning**: Configurable CloudWatch Event Rule triggers the Lambda function on a schedule.
-   **Tag-Based Categorization**: Uses specified tag keys to group resources.
-   **S3 Storage**: Stores generated constellation maps in an S3 bucket.
-   **IAM Least Privilege**: Lambda execution role with necessary permissions for scanning and S3 access.

## 🚀 Deployment

To deploy this module, you'll need Terraform installed and AWS credentials configured.

1.  **Initialize Terraform**:
    ```bash
    terraform init
    ```

2.  **Plan the deployment**:
    ```bash
    terraform plan
    ```

3.  **Apply the changes**:
    ```bash
    terraform apply
    ```

### Inputs

| Name                        | Description                                                               | Type     | Default                               | Required |
|-----------------------------|---------------------------------------------------------------------------|----------|---------------------------------------|----------|
| `aws_region`                | The AWS region to deploy resources into.                                  | `string` | `"us-east-1"`                       | no       |
| `project_name`              | A unique name for your project, used for resource naming and tagging.     | `string` | `"apocalypsai"`                     | no       |
| `project_tag_key`           | The tag key used to identify projects for constellation grouping.         | `string` | `"Project"`                         | no       |
| `environment_tag_key`       | The tag key used to identify environments for constellation grouping.     | `string` | `"Environment"`                     | no       |
| `scan_schedule_expression`  | The CloudWatch Event Rule schedule expression (e.g., `cron(0 0 * * ? *)` for daily at midnight UTC). | `string` | `"cron(0 0 * * ? *)"`               | no       |

### Outputs

| Name                     | Description                                    |
|--------------------------|------------------------------------------------|
| `lambda_function_name`   | The name of the deployed AWS Lambda function.  |
| `s3_data_bucket_name`    | The name of the S3 bucket storing constellation map data. |

## 🧪 Testing

This module includes a basic set of offline, deterministic tests to validate its configuration and ensure the expected resources are planned for creation.

To run the tests:

1.  Navigate to the `tests/` directory:
    ```bash
    cd tests/
    ```

2.  Execute the test script:
    ```bash
    ./test.sh
    ```

This script will perform `terraform init -backend=false`, `terraform validate`, and `terraform plan` against a test configuration, asserting the presence of key resources in the generated plan. It does not provision any actual AWS resources.
