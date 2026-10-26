# Nightly Cloud Whisperer Beacon

## Summary
This Terraform module provisions a secure, globally accessible static website beacon in AWS, designed for broadcasting short, vital messages or status updates to the community. It leverages AWS S3 for content storage and AWS CloudFront for global content delivery and HTTPS, acting as a digital campfire for survivors.

## Features
- **Static Website Hosting**: Utilizes AWS S3 to host `index.html` and `error.html` files.
- **Global Reach**: Employs AWS CloudFront for low-latency content delivery worldwide.
- **Secure Access**: Configures CloudFront Origin Access Identity (OAI) to restrict direct S3 bucket access, ensuring content is served only via CloudFront.
- **Customizable Message**: Allows setting a custom `beacon_message` that will be displayed on the `index.html` page.
- **HTTPS by Default**: CloudFront automatically provides HTTPS for secure communication.

## Usage
To use this module, include it in your Terraform configuration and provide the required variables.

### Prerequisites
- Terraform CLI installed (v1.0.0 or higher).
- AWS account and configured AWS credentials (e.g., via `~/.aws/credentials` or environment variables).

### Example `main.tf`
```terraform
module "apocalypsai_beacon" {
  source = "./nightly-cloud-whisper-beacon/src"

  project_name   = "apocalypsai-community"
  region         = "us-east-1"
  beacon_message = "Emergency Broadcast: The Integrator Agent has deployed a new utility! Stay tuned for updates."
}

output "beacon_url" {
  description = "The URL of the deployed Cloud Whisperer Beacon."
  value       = module.apocalypsai_beacon.cloudfront_domain_name
}
```

### Inputs
| Name             | Description                                                                 | Type   | Default                                                                       | Required |
|------------------|-----------------------------------------------------------------------------|--------|-------------------------------------------------------------------------------|----------|
| `project_name`   | A unique name for the project, used as a prefix for resources.              | `string` | n/a                                                                           | yes      |
| `region`         | The AWS region to deploy the beacon.                                        | `string` | `"us-east-1"`                                                                 | no       |
| `beacon_message` | The message content to display on the static website beacon.                | `string` | `"ApocalypsAI Nightly Integrator Beacon: All systems nominal. Stay vigilant."` | no       |
| `index_document` | The index document for the S3 static website.                               | `string` | `"index.html"`                                                                | no       |
| `error_document` | The error document for the S3 static website.                               | `string` | `"error.html"`                                                                | no       |

### Outputs
| Name                       | Description                                                     |
|----------------------------|-----------------------------------------------------------------|
| `cloudfront_domain_name`   | The domain name of the CloudFront distribution for the beacon.  |
| `s3_bucket_website_endpoint` | The S3 static website endpoint.                                 |

## Testing
This module includes automated tests that validate its Terraform configuration syntax and structure without deploying actual cloud resources.

To run the tests:

1. Navigate to the utility's root directory:
   `cd nightly-cloud-whisper-beacon`

2. Execute the test runner script:
   `bash tests/test_runner.sh`

This script will initialize Terraform in the test environment (without a backend) and run `terraform validate` to ensure the module's configuration is correct and all variables are properly referenced.

**Mock rationale**: The tests are designed to be deterministic and offline. `terraform validate` checks the syntax and internal consistency of the Terraform configuration without requiring AWS credentials or network access. A `null_resource` in `tests/test_main.tf` is used to simulate an assertion point for outputs, though its `local-exec` provisioner is not executed during `terraform validate`. This approach ensures the module's structure and variable usage are sound before any actual deployment.
