# Nightly Cloud Beacon

## Overview

The `nightly-cloud-beacon` is a whimsical-yet-useful Terraform module designed to deploy a highly-available, low-cost static website on AWS. Think of it as a digital distress signal or a friendly light in the vast, often confusing, digital wasteland. It provisions an S3 bucket for static content hosting and a CloudFront distribution to serve that content globally, ensuring resilience and reach.

This module is perfect for:
- Establishing a simple, public endpoint for connectivity tests.
- Demonstrating basic Infrastructure-as-Code (IaC) principles.
- Creating a symbolic 'presence' in a new AWS region or account.
- Having a reliable, low-maintenance 'hello world' resource.

## Features

- **AWS S3**: Secure and scalable storage for your static beacon content.
- **AWS CloudFront**: Global Content Delivery Network (CDN) for low-latency access and high availability.
- **Origin Access Control (OAC)**: Secure connection between CloudFront and S3.
- **Customizable Content**: Easily change the beacon's message.
- **Low Cost**: Designed for minimal operational expenses.

## Usage

To use this module, include it in your Terraform configuration and provide the necessary variables.

1.  **Create a `main.tf` file** (e.g., in a separate `environments/dev/` directory):

    ```terraform
    provider "aws" {
      region = "us-east-1" # Or your desired AWS region
    }

    module "my_cloud_beacon" {
      source = "./path/to/nightly-cloud-beacon/src" # Adjust this path

      bucket_name_prefix = "my-unique-beacon" # Must be globally unique
      region             = "us-east-1"        # Must match provider region
      content_body       = "ApocalypsAI is watching over you. Stay vigilant!"
      tags = {
        Environment = "Production"
        Project     = "ApocalypsAI"
        Owner       = "Community"
      }
    }

    output "beacon_url" {
      description = "The URL of the deployed CloudFront beacon."
      value       = module.my_cloud_beacon.cloudfront_domain_name
    }
    ```

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

5.  **Access your beacon**: After a few minutes (CloudFront deployment takes time), you can access your beacon using the `beacon_url` output.

## Inputs

| Name                 | Description                                      | Type         | Default                     | Required |
| :------------------- | :----------------------------------------------- | :----------- | :-------------------------- | :------- |
| `bucket_name_prefix` | A prefix for the S3 bucket name. Must be unique. | `string`     | `"apocalypsai-beacon"`     | `no`     |
| `region`             | The AWS region to deploy resources in.           | `string`     | `"us-east-1"`               | `no`     |
| `content_body`       | The main message to display on the beacon page.  | `string`     | `"ApocalypsAI Beacon: We are here."` | `no`     |
| `tags`               | A map of tags to apply to all resources.         | `map(string)`| `{}`                        | `no`     |

## Outputs

| Name                           | Description                                  |
| :----------------------------- | :------------------------------------------- |
| `s3_bucket_id`                 | The ID of the S3 bucket created.             |
| `cloudfront_domain_name`       | The domain name of the CloudFront distribution. |
| `cloudfront_distribution_id`   | The ID of the CloudFront distribution.       |

## Testing

The module includes a `tests/test.sh` script that performs offline validation and planning checks using `terraform init`, `terraform validate`, and `terraform plan`. It also verifies that the expected outputs are defined in the `src/outputs.tf` file.

To run the tests:

```bash
cd tests
./test.sh
```

**Note**: Running these tests requires `terraform` to be installed and available in your PATH. It does not require AWS credentials as it performs offline checks only.
