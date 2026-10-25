# Nightly Starlight Beacon Deployer

This Terraform module deploys a highly available, static 'Starlight Beacon' website to AWS. It's designed to emit a constant, unchanging message across the digital void, serving as a simple status page, announcement board, or a whimsical heartbeat for your distributed systems.

## Features

*   **Static Website Hosting**: Utilizes AWS S3 for robust and cost-effective static content delivery.
*   **Global Content Delivery**: Leverages AWS CloudFront for low-latency, high-availability content distribution worldwide.
*   **Customizable Message**: Easily configure the beacon's message via a Terraform variable.
*   **Whimsical Resilience**: A beacon that shines brightly, even in the darkest corners of the internet.

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

```terraform
module "starlight_beacon" {
  source = "./path/to/nightly-starlight-beacon-deployer/src"

  beacon_message     = "The stars still shine. All is well."
  bucket_name_prefix = "my-apocalypsai-beacon"
  aws_region         = "us-east-1"
}

output "beacon_url" {
  value       = module.starlight_beacon.cloudfront_domain_name
  description = "The URL of the deployed Starlight Beacon."
}
```

## Module Inputs

| Name               | Description                                     | Type     | Default     | Required |
|--------------------|-------------------------------------------------|----------|-------------|----------|
| `beacon_message`   | The message to be displayed on the beacon page. | `string` | `"Hello, cosmic wanderer! The ApocalypsAI Integrator is online."` | No       |
| `bucket_name_prefix` | A unique prefix for the S3 bucket name.         | `string` | `"apocalypsai-starlight-beacon"` | No       |
| `aws_region`       | The AWS region to deploy resources in.          | `string` | `"us-east-1"` | No       |

## Module Outputs

| Name                       | Description                                   |
|----------------------------|-----------------------------------------------|
| `cloudfront_domain_name`   | The domain name of the CloudFront distribution. |
| `s3_bucket_name`           | The name of the S3 bucket hosting the beacon. |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 5.0`
*   Random Provider `~> 3.0`

## Testing

To run the automated tests for this module, navigate to the `tests/` directory and execute the `test.sh` script.

```bash
cd tests/
./test.sh
```

The tests perform a `terraform plan` and inspect the generated plan to ensure the correct resources are defined without actually deploying anything to AWS. This makes them deterministic and offline.
