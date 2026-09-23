# Nightly Cloud-Whisperer Beacon

## Summary

This Terraform module provisions a low-cost, highly available static website on AWS, designed to serve as a "Cloud-Whisperer Beacon" for transmitting vital community messages across the digital wasteland. It leverages AWS S3 for content storage and AWS CloudFront for global content delivery, ensuring your whispers reach far and wide.

## Whimsical Context

In the fractured remnants of the old world, communication is a lifeline. The Cloud-Whisperer Beacon is a digital lighthouse, a persistent hum in the ether, broadcasting messages of hope, warnings of temporal anomalies, or even just whimsical musings to any survivor who stumbles upon its frequency. Deploy it, customize its message, and keep the spirit of connection alive!

## Features

*   **Static Website Hosting:** Uses AWS S3 to store `index.html` and `error.html` files.
*   **Global Content Delivery:** Leverages AWS CloudFront for low-latency, high-availability content distribution with HTTPS.
*   **Secure S3 Access:** CloudFront uses an Origin Access Identity (OAI) to securely fetch content from S3, keeping the bucket private.
*   **Cost-Effective:** Designed for minimal operational cost, ideal for long-term, low-traffic communication.
*   **Customizable:** Easily update the `index.html` and `error.html` content to broadcast your own messages.

## Prerequisites

*   [Terraform CLI](https://www.terraform.io/downloads.html) installed (v1.0.0+).
*   [AWS CLI](https://aws.amazon.com/cli/) configured with credentials that have permissions to create S3 buckets, CloudFront distributions, and IAM resources.

## Usage

1.  **Navigate to the `src` directory:**
    ```bash
    cd src
    ```

2.  **Initialize Terraform:**
    This downloads the necessary AWS provider.
    ```bash
    terraform init
    ```

3.  **Review and Customize Variables:**
    Open `variables.tf` and consider overriding the default values, especially `content_bucket_name`, which **must be globally unique** across all AWS S3 buckets.

4.  **Generate a Terraform Plan:**
    This command shows you what resources Terraform will create without actually making any changes. Replace `your-unique-bucket-name` with a truly unique name.
    ```bash
    terraform plan -var="content_bucket_name=your-unique-beacon-bucket-name"
    ```

5.  **Apply the Terraform Configuration:**
    If the plan looks good, apply it to provision the resources.
    ```bash
    terraform apply -var="content_bucket_name=your-unique-beacon-bucket-name"
    ```
    Type `yes` when prompted to confirm.

6.  **Retrieve the Beacon URL:**
    After successful application, Terraform will output the CloudFront domain name.
    ```bash
    terraform output cloudfront_domain_name
    ```
    Navigate to this URL in your browser to see your Cloud-Whisperer Beacon in action!

7.  **Destroy the Beacon (Optional):**
    When the beacon's message has been heard, or if you need to dismantle it, run:
    ```bash
    terraform destroy -var="content_bucket_name=your-unique-beacon-bucket-name"
    ```
    Type `yes` when prompted to confirm.

## Inputs

| Name                | Description                                                              | Type   | Default                                   | Required |
| :------------------ | :----------------------------------------------------------------------- | :----- | :---------------------------------------- | :------- |
| `project_name`      | A unique name for your project, used in resource tagging and naming.     | `string` | `"apocalypsai-beacon"`                    | no       |
| `aws_region`        | The AWS region to deploy resources in.                                   | `string` | `"us-east-1"`                             | no       |
| `content_bucket_name` | The name for the S3 bucket that will host the beacon content. Must be globally unique. | `string` | `"apocalypsai-whisperer-beacon-content-unique-name"` | no       |

## Outputs

| Name                       | Description                                                               | Sensitive |
| :------------------------- | :------------------------------------------------------------------------ | :-------- |
| `cloudfront_domain_name`   | The domain name of the CloudFront distribution, where your beacon will be accessible. | no        |
| `s3_bucket_name`           | The name of the S3 bucket hosting the beacon content.                     | no        |

## Customizing Content

You can modify the `src/content/index.html` and `src/content/error.html` files to change the messages broadcast by your beacon. After modifying, run `terraform apply` again to upload the new content to S3 and invalidate CloudFront's cache (though CloudFront's default TTLs might mean a slight delay before changes are visible globally).
