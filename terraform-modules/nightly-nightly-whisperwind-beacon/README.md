# Nightly Whisperwind Beacon

The Nightly Whisperwind Beacon is a Terraform module designed to provision an ephemeral, secure communication beacon in the AWS cloud. In the digital wasteland, reliable communication is a fleeting luxury. This beacon provides a temporary, configurable endpoint to broadcast messages of hope, relay critical survival data, or simply serve as a transient marker in the vast expanse of the internet.

It sets up a minimal EC2 instance running a simple web server, an S3 bucket for storing beacon logs or messages, and the necessary security configurations.

## Features

*   **Ephemeral**: Easily provisioned and destroyed, perfect for temporary communication needs.
*   **Configurable Message**: Broadcast a custom message of your choosing.
*   **Secure**: Configurable security group for controlled access.
*   **Logging**: Integrates with an S3 bucket for persistent storage of beacon activity or messages.
*   **AWS-Native**: Leverages standard AWS services for reliability.

## Usage

To deploy a Whisperwind Beacon, include this module in your Terraform configuration:

```terraform
module "whisperwind_beacon" {
  source = "./nightly-whisperwind-beacon/src" # Adjust path if not local

  region          = "us-east-1"
  instance_type   = "t2.micro"
  ami_id          = "ami-0abcdef1234567890" # Replace with a valid AMI for your region (e.g., Amazon Linux 2)
  key_name        = "my-ssh-key"          # Replace with your EC2 Key Pair name
  beacon_message  = "Hope endures, even in the digital void."
  beacon_port     = 8080
  tags = {
    Project = "ApocalypsAI"
    Purpose = "WhisperwindBeacon"
  }
}

output "beacon_public_ip" {
  description = "The public IP address of the Whisperwind Beacon."
  value       = module.whisperwind_beacon.public_ip
}

output "beacon_s3_bucket_name" {
  description = "The name of the S3 bucket for beacon logs/messages."
  value       = module.whisperwind_beacon.s3_bucket_name
}
```

### Prerequisites

*   Terraform CLI installed.
*   AWS CLI configured with appropriate credentials and default region.
*   An existing EC2 Key Pair in your chosen AWS region.
*   A valid AMI ID for your chosen region (e.g., `ami-0abcdef1234567890` is a placeholder, find a suitable Amazon Linux 2 or Ubuntu AMI).

### Deployment Steps

1.  Navigate to your Terraform project directory.
2.  Initialize Terraform: `terraform init`
3.  Review the plan: `terraform plan`
4.  Apply the configuration: `terraform apply`

### Destruction

To tear down the beacon and all associated resources:

`terraform destroy`

## Module Inputs

| Name            | Description                                     | Type     | Default       | Required |
| :-------------- | :---------------------------------------------- | :------- | :------------ | :------- |
| `region`        | AWS region to deploy resources into.            | `string` | n/a           | yes      |
| `instance_type` | EC2 instance type for the beacon.               | `string` | `"t2.micro"`  | no       |
| `ami_id`        | AMI ID for the EC2 instance.                    | `string` | n/a           | yes      |
| `key_name`      | EC2 Key Pair name for SSH access.               | `string` | n/a           | yes      |
| `beacon_message`| The message the beacon will broadcast.          | `string` | `"Echoing hope across the digital wasteland."` | no |
| `beacon_port`   | The port on which the beacon web server will run.| `number` | `8080`        | no       |
| `tags`          | A map of tags to apply to all resources.        | `map(string)` | `{}`          | no       |

## Module Outputs

| Name                  | Description                                     |
| :-------------------- | :---------------------------------------------- |
| `public_ip`           | The public IP address of the EC2 beacon instance. |
| `s3_bucket_name`      | The name of the S3 bucket created for the beacon. |
| `security_group_id`   | The ID of the security group created.           |
