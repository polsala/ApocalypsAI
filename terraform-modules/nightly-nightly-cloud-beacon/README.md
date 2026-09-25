# Nightly Cloud Beacon

## Summary

The `nightly-cloud-beacon` is a whimsical yet highly useful Terraform module designed to provision a simple, resilient web server and an S3 bucket in AWS. This 'Cloud Beacon' acts as a digital lighthouse in the post-apocalyptic cloud, broadcasting vital community messages and archiving important logs or updates.

It's perfect for establishing a quick, reliable communication point for survivors, or simply for broadcasting a daily dose of hope (or warnings).

## Features

*   **Simple Web Server**: Deploys an EC2 instance running Nginx to serve a customizable beacon message.
*   **Static IP**: Uses an Elastic IP for a consistent public address.
*   **Message Archive**: Provisions an S3 bucket for storing logs, additional messages, or important community files.
*   **Network Isolation**: Creates a dedicated VPC, subnet, and security group for secure operation.
*   **Customizable**: Easily configure the AWS region, instance type, and the beacon's message.

## Usage

To use this module, include it in your root Terraform configuration and provide the necessary variables.

### Prerequisites

*   Terraform CLI (v1.6.0 or higher)
*   AWS Account and configured AWS CLI credentials (or environment variables)

### Example `main.tf`

Create a `main.tf` file in your working directory:

```terraform
provider "aws" {
  region = "us-east-1"
}

module "cloud_beacon" {
  source = "./nightly-cloud-beacon/src" # Adjust path if not in a subdirectory

  region         = "us-east-1"
  instance_type  = "t2.micro"
  beacon_message = "Attention all survivors: The ApocalypsAI Integrator is active. Stay safe!"
  key_name       = "your-ssh-key-name" # Optional: provide an existing EC2 Key Pair name for SSH access
}

output "beacon_ip" {
  value       = module.cloud_beacon.beacon_public_ip
  description = "The public IP address of the Cloud Beacon."
}

output "beacon_url" {
  value       = module.cloud_beacon.beacon_url
  description = "The URL to access the Cloud Beacon."
}

output "archive_bucket" {
  value       = module.cloud_beacon.s3_bucket_name
  description = "The name of the S3 bucket for beacon message archives."
}
```

### Deployment Steps

1.  **Initialize Terraform**: `terraform init`
2.  **Plan Deployment**: `terraform plan`
3.  **Apply Changes**: `terraform apply`

After applying, the outputs will display the public IP, URL, and S3 bucket name for your Cloud Beacon.

## Inputs

| Name             | Description                                                                                             | Type   | Default                                            | Required |
| :--------------- | :------------------------------------------------------------------------------------------------------ | :----- | :------------------------------------------------- | :------- |
| `region`         | The AWS region to deploy the beacon.                                                                    | `string` | `"us-east-1"`                                      | no       |
| `instance_type`  | The EC2 instance type for the beacon server.                                                            | `string` | `"t2.micro"`                                       | no       |
| `key_name`       | The name of an existing EC2 Key Pair to allow SSH access to the beacon server. Leave empty if no SSH access is desired. | `string` | `""`                                               | no       |
| `beacon_message` | The message to be displayed on the Cloud Beacon's webpage.                                              | `string` | `"Seeking survivors. All systems nominal. Stay vigilant."` | no       |

## Outputs

| Name                 | Description                                       |
| :------------------- | :------------------------------------------------ |
| `beacon_public_ip`   | The public IP address of the Cloud Beacon.        |
| `beacon_url`         | The URL to access the Cloud Beacon.               |
| `s3_bucket_name`     | The name of the S3 bucket for beacon message archives. |

## Testing

This module includes unit tests using Terraform's built-in testing framework. These tests use mock providers to simulate AWS resources, ensuring they are deterministic and do not incur cloud costs.

To run the tests:

```bash
terraform -chdir=./nightly-cloud-beacon/src test
```

(Adjust the `-chdir` path if your module is located differently relative to your current directory.)
