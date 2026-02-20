# Nightly Cloud Scavenger

A Terraform module designed to provision essential, cost-effective AWS cloud resources for the discerning survivor. Perfect for setting up a small data cache, a communication relay, or a temporary compute node in the vast digital wasteland. This module focuses on minimal viable infrastructure to conserve precious credits and resources.

## Features

*   **S3 Data Cache**: An S3 bucket configured for versioning and lifecycle rules to transition data to cheaper storage classes (Standard-IA, Glacier) and eventually expire it, optimizing for cost.
*   **EC2 Communication Relay**: A basic EC2 instance (defaulting to `t3.nano`) with a security group allowing SSH access, suitable for a lightweight communication node or processing unit.

## Usage

### Prerequisites

*   [Terraform](https://www.terraform.io/downloads.html) installed.
*   [AWS CLI](https://aws.amazon.com/cli/) configured with appropriate credentials and default region.

### Example `main.tf`

Create a new directory for your outpost and add a `main.tf` file:

```terraform
module "scavenged_outpost" {
  source = "./path/to/nightly-cloud-scavenger" # Adjust this path to where you place the module

  prefix            = "apocalypsai-outpost"
  region            = "us-east-1"
  enable_s3_cache   = true
  enable_ec2_relay  = true
  ec2_instance_type = "t3.nano"
  ec2_ami_id        = "ami-053b0d53d79155700" # Example Amazon Linux 2 AMI for us-east-1, find current one for your region
  ec2_key_name      = "my-apocalypsai-key" # IMPORTANT: Replace with an existing EC2 Key Pair name
}

output "s3_bucket_name" {
  value = module.scavenged_outpost.s3_bucket_name
}

output "ec2_public_ip" {
  value = module.scavenged_outpost.ec2_public_ip
}
```

### Deployment Steps

1.  **Initialize Terraform**: Navigate to your outpost directory and run:
    ```bash
    terraform init
    ```
2.  **Review the Plan**: See what resources Terraform will create:
    ```bash
    terraform plan
    ```
3.  **Apply the Configuration**: Provision the resources:
    ```bash
    terraform apply
    ```
    Confirm with `yes` when prompted.

4.  **Destroy Resources (Cleanup)**: When the outpost is no longer needed, clean up all resources:
    ```bash
    terraform destroy
    ```
    Confirm with `yes` when prompted.

## Inputs

| Name                | Description                                                               | Type    | Default               | Required |
| :------------------ | :------------------------------------------------------------------------ | :------ | :-------------------- | :------- |
| `prefix`            | A prefix for all resource names to ensure uniqueness and identification.  | `string`| `"apocalypsai"`      | no       |
| `region`            | The AWS region where resources will be provisioned.                       | `string`| `"us-east-1"`         | no       |
| `enable_s3_cache`   | Set to `true` to provision an S3 bucket for data caching.                 | `bool`  | `true`                | no       |
| `enable_ec2_relay`  | Set to `true` to provision an EC2 instance for communication relay.       | `bool`  | `true`                | no       |
| `ec2_instance_type` | The instance type for the EC2 relay node (e.g., `t3.nano`, `t2.micro`).   | `string`| `"t3.nano"`           | no       |
| `ec2_ami_id`        | The AMI ID for the EC2 relay node. Provide a suitable AMI for your chosen region. | `string`| `"ami-0abcdef1234567890"` | no       |
| `ec2_key_name`      | The name of the EC2 Key Pair to associate with the relay node. Must exist in the target region. | `string`| `"apocalypsai-keypair"` | no       |

## Outputs

| Name             | Description                                          |
| :--------------- | :--------------------------------------------------- |
| `s3_bucket_name` | The name of the provisioned S3 data cache bucket.    |
| `ec2_public_ip`  | The public IP address of the EC2 communication relay node. |
