# Nightly Cloud Sanctuary Beacon

This Terraform module provisions a highly available and secure static website beacon in AWS, designed to broadcast vital post-apocalyptic messages, "safe zone" statuses, or simply serve as a persistent signal of hope in the digital wasteland. It leverages AWS S3 for static website hosting and AWS CloudFront for global content delivery, caching, and HTTPS.

## Features

*   **Static Website Hosting**: Utilizes AWS S3 for cost-effective and scalable content storage.
*   **Global Reach**: AWS CloudFront distributes your beacon content worldwide with low latency.
*   **HTTPS by Default**: CloudFront ensures secure communication.
*   **Customizable Content**: Easily update the `index.html` or other static files.
*   **Secure S3 Access**: Uses CloudFront Origin Access Control (OAC) for secure S3 bucket access.

## Prerequisites

*   An AWS account with appropriate permissions to create S3 buckets, CloudFront distributions, and IAM policies.
*   [Terraform CLI](https://www.terraform.io/downloads.html) installed (v1.0+ recommended).
*   AWS credentials configured (e.g., via `~/.aws/credentials` or environment variables).

## Usage

1.  **Initialize Terraform**:
    ```bash
    terraform init
    ```

2.  **Review the Plan**:
    ```bash
    terraform plan
    ```
    This will show you the infrastructure Terraform plans to create.

3.  **Apply the Configuration**:
    ```bash
    terraform apply
    ```
    Confirm with `yes` when prompted.

4.  **Access Your Beacon**:
    After successful deployment, Terraform will output the CloudFront domain name. Navigate to this URL in your browser to see your sanctuary beacon!

    ```
    Outputs:

    cloudfront_domain_name = "d12345abcdef.cloudfront.net"
    ```

5.  **Update Content**:
    To update the content, modify the `src/index.html` file (or add other static assets) and re-run `terraform apply`. Terraform will detect the changes and update the S3 bucket.

6.  **Destroy the Beacon**:
    When the beacon is no longer needed (or for testing purposes), you can destroy all provisioned resources:
    ```bash
    terraform destroy
    ```
    Confirm with `yes` when prompted.

## Module Structure

```
.
├── README.md
├── src/
│   ├── main.tf           # Core AWS resource definitions (S3, CloudFront, OAC)
│   ├── variables.tf      # Input variables for customization
│   ├── outputs.tf        # Output values (e.g., CloudFront domain)
│   └── index.html        # Default static content for the beacon
└── tests/
    └── test_plan.md      # Instructions for validating the Terraform module
```
