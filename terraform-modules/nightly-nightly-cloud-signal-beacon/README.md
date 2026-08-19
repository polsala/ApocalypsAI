# Nightly Cloud Signal Beacon

This Terraform module provisions a simple, highly-available static website on AWS S3, configured to act as a "cloud signal beacon." It emits a customizable message, serving as a whimsical 'all-clear' or 'presence' signal across the digital wasteland.

## Features

*   **Static Website Hosting**: Utilizes AWS S3 for cost-effective and resilient static content delivery.
*   **Customizable Message**: Inject a unique "signal message" into the beacon's homepage.
*   **Publicly Accessible**: Configured for public read access, ensuring the signal reaches all corners.
*   **Whimsical Output**: The beacon's page includes a dynamic timestamp and your custom message.

## Usage

1.  **Configure AWS Credentials**: Ensure your AWS CLI or environment variables are configured with appropriate credentials that have permissions to create S3 buckets and objects.

2.  **Create a `main.tf` file**: In your Terraform project, create a `main.tf` file and include this module:

    ```terraform
    provider "aws" {
      region = "us-east-1" # Or your desired AWS region
    }

    module "signal_beacon" {
      source = "./terraform-modules/nightly-cloud-signal-beacon/src"

      region             = "us-east-1" # Must match provider region
      bucket_name_prefix = "apocalypsai-beacon-alpha" # Unique prefix for your S3 bucket
      signal_message     = "The void whispers, but we endure! All systems nominal."
    }

    output "beacon_url" {
      description = "The URL of the deployed cloud signal beacon."
      value       = module.signal_beacon.website_endpoint
    }
    ```

3.  **Initialize Terraform**:

    ```bash
    terraform init
    ```

4.  **Plan and Apply**: Review the changes and deploy the beacon.

    ```bash
    terraform plan
    terraform apply
    ```

5.  **Access the Beacon**: After successful application, the `beacon_url` output will provide the URL to your deployed signal beacon.

## Module Inputs

| Name               | Description                                   | Type     | Default | Required |
| :----------------- | :-------------------------------------------- | :------- | :------ | :------- |
| `region`           | The AWS region to deploy the S3 bucket in.    | `string` | n/a     | yes      |
| `bucket_name_prefix` | A unique prefix for the S3 bucket name. The full bucket name will be generated using this prefix and a unique ID. | `string` | n/a     | yes      |
| `signal_message`   | The whimsical message to display on the beacon's page. | `string` | n/a     | yes      |

## Module Outputs

| Name             | Description                                   | Value |
| :--------------- | :-------------------------------------------- | :---- |
| `website_endpoint` | The S3 static website endpoint URL for the beacon. | `string` |

## Cleanup

To destroy the deployed resources:

```bash
terraform destroy
```
