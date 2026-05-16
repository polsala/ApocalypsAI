# Nightly Cloud Sanctuary Beacon

This Terraform module provisions a highly available and resilient static website in AWS, designed to act as a 'sanctuary beacon' in the digital wasteland. It's perfect for broadcasting comforting messages, critical updates, or simply a persistent signal of hope.

## Features

*   **Static Content Hosting**: Utilizes AWS S3 for cost-effective and scalable static content storage.
*   **Global Content Delivery**: Leverages AWS CloudFront for low-latency content delivery, HTTPS encryption, and enhanced security via Origin Access Control (OAC).
*   **High Availability**: Designed with cloud-native services for inherent resilience.
*   **Customizable Content**: Easily update the `index.html` or provide your own content.

## Usage

To deploy your own Cloud Sanctuary Beacon, include this module in your Terraform configuration:

```terraform
module "sanctuary_beacon" {
  source = "./path/to/nightly-cloud-sanctuary-beacon/src"

  project_name      = "apocalypsai-beacon"
  environment       = "prod"
  content_file_path = "./path/to/your/content/index.html" # Optional: path to your local HTML file
}

output "beacon_url" {
  description = "The URL of your Cloud Sanctuary Beacon."
  value       = module.sanctuary_beacon.cloudfront_domain_name
}
```

### Inputs

| Name                | Description                                                              | Type     | Default                                | Required |
|---------------------|--------------------------------------------------------------------------|----------|----------------------------------------|----------|
| `project_name`      | A unique name for your project, used to prefix resource names.           | `string` | `"apocalypsai"`                        | no       |
| `environment`       | The deployment environment (e.g., `dev`, `prod`).                        | `string` | `"dev"`                                | no       |
| `content_file_path` | Path to the local HTML file to upload as the beacon's content.           | `string` | `"${path.module}/content/index.html"` | no       |

### Outputs

| Name                     | Description                                     |
|--------------------------|-------------------------------------------------|
| `cloudfront_domain_name` | The domain name of the CloudFront distribution. |
| `s3_bucket_name`         | The name of the S3 bucket hosting the content.  |

## Requirements

*   [Terraform](https://www.terraform.io/downloads.html) (>= 1.0)
*   [AWS CLI](https://aws.amazon.com/cli/) configured with appropriate credentials and permissions to create S3 buckets, CloudFront distributions, and IAM policies.

## Running Tests

Navigate to the `tests/` directory and run:

```bash
terraform init
terraform test
```

This will run the module with mock inputs and assert that the expected resources and outputs are generated correctly without deploying actual cloud resources. The tests are designed to be deterministic and offline.
