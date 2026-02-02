# Nightly Wasteland Resource Beacon

This Terraform module provisions a 'Wasteland Resource Beacon' in AWS. It creates a minimal EC2 instance with a public IP and an S3 bucket, designed to be a discoverable waypoint or communication hub for other agents or services in a post-apocalyptic scenario (or just a simple, ephemeral sandbox).

## Features

*   **Discoverable EC2 Instance**: A `t2.micro` instance with a public IP, allowing for easy access and serving as a visible presence.
*   **Secure Access**: Configurable security group for SSH and a custom beacon port.
*   **S3 Beacon Storage**: A dedicated S3 bucket for storing messages, logs, or configuration data that other agents can retrieve.
*   **Output**: Provides the public IP of the EC2 instance and the S3 bucket details for easy integration.

## Usage

To deploy your Wasteland Resource Beacon, create a `main.tf` file in your project directory and reference this module:

```terraform
module "wasteland_beacon" {
  source = "./path/to/nightly-wasteland-beacon" # Adjust path as needed

  region        = "us-east-1"
  instance_type = "t2.micro"
  ami_id        = "ami-0abcdef1234567890" # Replace with a valid AMI for your region (e.g., Amazon Linux 2 AMI)
  key_name      = "my-ssh-key"          # Replace with your EC2 Key Pair name
  beacon_port   = 8080

  tags = {
    Project     = "ApocalypsAI"
    Environment = "Dev"
    BeaconName  = "AlphaBeacon"
  }
}

output "beacon_ip" {
  value       = module.wasteland_beacon.beacon_public_ip
  description = "The public IP address of the Wasteland Beacon EC2 instance."
}

output "beacon_s3_bucket" {
  value       = module.wasteland_beacon.beacon_s3_bucket_name
  description = "The name of the S3 bucket for beacon messages."
}

output "beacon_s3_endpoint" {
  value       = module.wasteland_beacon.beacon_s3_bucket_endpoint
  description = "The endpoint URL for the S3 bucket."
}
```

Then, run the standard Terraform commands:

```bash
terraform init
terraform plan
terraform apply
```

## Inputs

| Name            | Description                                        | Type     | Default       | Required |
|-----------------|----------------------------------------------------|----------|---------------|----------|
| `region`        | AWS region to deploy resources into.               | `string` | `"us-east-1"` | no       |
| `instance_type` | EC2 instance type for the beacon.                  | `string` | `"t2.micro"`  | no       |
| `ami_id`        | AMI ID for the EC2 instance.                       | `string` | n/a           | yes      |
| `key_name`      | EC2 Key Pair name for SSH access.                  | `string` | n/a           | yes      |
| `beacon_port`   | Custom TCP port for the beacon signal.             | `number` | `8080`        | no       |
| `tags`          | A map of tags to apply to all created resources.   | `map`    | `{}`          | no       |

## Outputs

| Name                        | Description                                          |
|-----------------------------|------------------------------------------------------|
| `beacon_public_ip`          | The public IP address of the Wasteland Beacon EC2 instance. |
| `beacon_s3_bucket_name`     | The name of the S3 bucket for beacon messages.       |
| `beacon_s3_bucket_endpoint` | The endpoint URL for the S3 bucket.                  |

## Testing

Refer to `tests/test_plan.sh` for an example of how to run offline, deterministic tests using `terraform plan` and `jq` to verify the module's output without deploying actual resources.
