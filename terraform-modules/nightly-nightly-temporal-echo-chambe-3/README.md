# Nightly Temporal Echo Chamber (Terraform Module)

This Terraform module provisions a highly available and low-cost static website infrastructure on AWS, perfect for broadcasting ephemeral "temporal echoes" – short, whimsical messages or survival tips that might fade or change over time. It leverages AWS S3 for storage and CloudFront for global content delivery, ensuring your echoes reach every corner of the post-apocalyptic wasteland with minimal latency.

## Features

*   **Ephemeral Broadcasts**: Infrastructure optimized for static content, ideal for messages that are updated frequently or have a short shelf-life.
*   **Global Reach**: CloudFront CDN ensures your messages are delivered quickly to users worldwide.
*   **High Availability**: S3 and CloudFront are designed for extreme durability and uptime.
*   **Cost-Effective**: Pay-as-you-go model, with S3 and CloudFront being very economical for static content.
*   **Secure**: Uses CloudFront Origin Access Control (OAC) to restrict direct S3 bucket access.

## Usage

To deploy your own Temporal Echo Chamber, create a `main.tf` file in your Terraform project:

```terraform
module "temporal_echo_chamber" {
  source = "./path/to/nightly-temporal-echo-chamber-tf/src" # Adjust path as needed

  bucket_name_prefix = "apocalypsai-echo"
  content_html       = "<h1>Welcome, Wanderer!</h1><p>The echoes whisper of a new dawn...</p><p>Current temporal distortion: Minimal.</p>"
  tags = {
    Project     = "ApocalypsAI"
    Environment = "Production"
    Utility     = "TemporalEchoChamber"
  }
}

output "echo_chamber_url" {
  description = "The URL of the Temporal Echo Chamber CloudFront distribution."
  value       = module.temporal_echo_chamber.cloudfront_domain_name
}
```

### Inputs

| Name                 | Description                                                                 | Type     | Default | Required |
| :------------------- | :-------------------------------------------------------------------------- | :------- | :------ | :------- |
| `bucket_name_prefix` | A prefix for the S3 bucket name. A unique suffix will be appended.          | `string` | `null`  | yes      |
| `content_html`       | The initial HTML content for the `index.html` file in the S3 bucket.        | `string` | `null`  | yes      |
| `tags`               | A map of tags to apply to all resources created by the module.              | `map`    | `{}`    | no       |

### Outputs

| Name                     | Description                                                              |
| :----------------------- | :----------------------------------------------------------------------- |
| `cloudfront_domain_name` | The domain name of the CloudFront distribution.                          |
| `s3_bucket_website_endpoint` | The S3 static website endpoint (for direct access, not recommended). |

## Prerequisites

*   An AWS account configured with appropriate credentials.
*   Terraform CLI installed (v1.0+ recommended).

## Running Tests

The module includes a simple shell script to validate its syntax and structure offline.

```bash
cd nightly-temporal-echo-chamber-tf
./tests/test_module.sh
```

This script will run `terraform init` and `terraform validate` to check for syntax errors and correct module configuration. It also performs a `terraform plan` to ensure expected resources are generated.
