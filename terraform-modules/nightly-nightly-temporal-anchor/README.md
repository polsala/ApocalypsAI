# Nightly Temporal Anchor

## Summary

The `nightly-temporal-anchor` utility provisions a resilient static website on AWS S3 and CloudFront. In the chaotic digital landscape of ApocalypsAI, this serves as a stable, immutable point, broadcasting a fixed message or a 'stabilized' timestamp to reassure the community. It's a digital lighthouse in the storm.

## Features

*   **Static Website Hosting**: Utilizes AWS S3 for highly available and durable content storage.
*   **Global Content Delivery**: Leverages AWS CloudFront for low-latency content delivery and DDoS protection.
*   **Secure Access**: Configures an Origin Access Identity (OAI) to restrict direct S3 bucket access, ensuring content is served only via CloudFront.
*   **Customizable Content**: Easily update the `index.html` file to change the anchor's message.
*   **Infrastructure as Code**: Fully defined using Terraform for repeatable and version-controlled deployments.

## Prerequisites

Before you can use this utility, you need:

1.  **Terraform CLI**: Installed and configured on your local machine (version 1.0+).
2.  **AWS Account**: An active AWS account.
3.  **AWS CLI & Credentials**: Configured with appropriate permissions to create S3 buckets, CloudFront distributions, and IAM policies. Ensure your AWS credentials are set up (e.g., via `~/.aws/credentials` or environment variables).

## Usage

1.  **Navigate to the module directory**:
    ```bash
    cd terraform-modules/nightly-temporal-anchor/src
    ```

2.  **Initialize Terraform**: This downloads the necessary AWS provider plugins.
    ```bash
    terraform init
    ```

3.  **Review the plan**: See what infrastructure Terraform will create.
    ```bash
    terraform plan
    ```

4.  **Apply the configuration**: Deploy the resources to your AWS account.
    ```bash
    terraform apply
    ```
    Confirm with `yes` when prompted.

5.  **Access the Anchor**: After successful deployment, Terraform will output the `cloudfront_domain_name`. Navigate to this URL in your browser to see your temporal anchor.

6.  **Destroy the infrastructure**: When you no longer need the anchor, you can tear down all resources.
    ```bash
    terraform destroy
    ```
    Confirm with `yes` when prompted.

## Customization

*   **`src/variables.tf`**: Adjust `bucket_name_prefix` to change the S3 bucket name. Ensure it's globally unique.
*   **`src/content/index.html`**: Modify this file to change the message displayed by your temporal anchor. You can also add other static assets (CSS, JS, images) and update the S3 sync command accordingly.

## Example Output

```
Apply complete! Resources: 4 added, 0 changed, 0 destroyed.

Outputs:

cloudfront_domain_name = "d12345abcdef.cloudfront.net"
```
