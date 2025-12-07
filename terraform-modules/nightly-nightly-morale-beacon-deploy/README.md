# Nightly Morale Beacon Deployer

This Terraform module deploys a serverless "Morale Beacon" to AWS. The beacon consists of an AWS Lambda function exposed via API Gateway, which serves uplifting messages to anyone who queries it. It's designed to be a simple, resilient, and low-cost way to broadcast positivity in the post-apocalyptic digital wasteland.

## Features

*   **Serverless:** No servers to manage, scales automatically.
*   **Cost-Effective:** Pay only for invocations.
*   **Customizable Messages:** Easily update the list of uplifting messages.
*   **API Endpoint:** Provides a simple HTTP GET endpoint to retrieve a random message.

## Usage

1.  **Configure AWS Credentials:** Ensure your AWS CLI or environment variables are configured with appropriate credentials.
2.  **Initialize Terraform:**
    ```bash
    terraform init
    ```
3.  **Review the Plan:**
    ```bash
    terraform plan
    ```
4.  **Deploy the Beacon:**
    ```bash
    terraform apply
    ```

    You will be prompted to confirm the deployment.

5.  **Access the Beacon:**
    After successful deployment, the API Gateway endpoint URL will be available in the Terraform outputs.
    ```bash
    terraform output beacon_url
    ```
    You can then access this URL using `curl` or a web browser:
    ```bash
    curl $(terraform output -raw beacon_url)/message
    ```

## Module Inputs

| Name                 | Description                                       | Type           | Default                               |
| :------------------- | :------------------------------------------------ | :------------- | :------------------------------------ |
| `project_name`       | A unique name for the project, used for resource naming. | `string`       | `"morale-beacon"`                     |
| `aws_region`         | The AWS region to deploy resources into.          | `string`       | `"us-east-1"`                         |
| `uplifting_messages` | A list of strings, each an uplifting message.     | `list(string)` | `["Stay strong!", "Hope endures!", "We'll rebuild!"]` |

## Outputs

| Name         | Description                                   |
| :----------- | :-------------------------------------------- |
| `beacon_url` | The URL of the deployed API Gateway endpoint. |

## Development & Testing

The module includes `terraform validate` and `terraform fmt` checks for syntax and formatting. The Lambda function has its own Python unit tests.

To run the tests:
```bash
chmod +x tests/test_terraform.sh
./tests/test_terraform.sh
python3 -m unittest tests/test_lambda.py
```
