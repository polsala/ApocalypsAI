# Nightly Cloud Critter Comfort Zone

This Terraform module provisions a small, isolated AWS EC2 instance designed to host a whimsical 'critter' application. The critter is a simple web server that, upon launch, sets up an Apache HTTP server and serves a random, comforting message to anyone who visits its public IP address.

It's a delightful way to deploy a tiny, low-resource digital companion in the cloud, offering a moment of whimsy in the vast digital wasteland.

## Features

*   **Isolated Environment**: Deploys an EC2 instance within a specified VPC and secures it with a dedicated security group.
*   **Whimsical Web Server**: Automatically configures an Apache web server on launch, serving a random comforting message.
*   **Customizable Critter**: Allows you to name your critter, which will appear in its welcome message and resource tags.
*   **Basic Connectivity**: Opens ports 22 (SSH) and 80 (HTTP) to the world (configurable via security group rules).

## Usage

To use this module, you need an AWS account, a configured AWS CLI/provider, an existing VPC, and an EC2 Key Pair.

1.  **Create a `main.tf` file** in your project directory:

    ```terraform
    provider "aws" {
      region = "us-east-1" # Or your desired AWS region
    }

    resource "aws_key_pair" "critter_key" {
      key_name   = "my-critter-key"
      public_key = "ssh-rsa AAAAB3NzaC... your_public_key_here"
    }

    # Example: Find a default VPC ID or use an existing one
    data "aws_vpc" "selected" {
      default = true
    }

    module "my_first_critter" {
      source = "./path/to/nightly-cloud-critter-zone" # Adjust this path

      ami_id        = "ami-0abcdef1234567890" # Replace with a valid AMI for your region (e.g., Amazon Linux 2 AMI)
      instance_type = "t2.micro"
      key_pair_name = aws_key_pair.critter_key.key_name
      vpc_id        = data.aws_vpc.selected.id
      critter_name  = "WhisperBot"
    }

    output "critter_ip" {
      description = "The public IP address of your Cloud Critter."
      value       = module.my_first_critter.instance_public_ip
    }
    ```

2.  **Initialize Terraform**:

    ```bash
    terraform init
    ```

3.  **Review the plan**:

    ```bash
    terraform plan
    ```

4.  **Apply the configuration**:

    ```bash
    terraform apply
    ```

    After applying, Terraform will output the public IP address of your critter. Navigate to this IP in your web browser to receive your comforting message!

5.  **Clean up** (when your critter needs a nap):

    ```bash
    terraform destroy
    ```

## Inputs

| Name            | Description                                                | Type     | Default             | Required |
| :-------------- | :--------------------------------------------------------- | :------- | :------------------ | :------- |
| `ami_id`        | The AMI ID for the EC2 instance.                           | `string` | `ami-0abcdef1234567890` | yes      |
| `instance_type` | The EC2 instance type.                                     | `string` | `t2.micro`            | no       |
| `key_pair_name` | The name of the EC2 Key Pair to allow SSH access.          | `string` | n/a                 | yes      |
| `vpc_id`        | The ID of the VPC where the critter instance will be deployed. | `string` | n/a                 | yes      |
| `critter_name`  | A whimsical name for your cloud critter.                   | `string` | `Whimsy`              | no       |

## Outputs

| Name                  | Description                                        |
| :-------------------- | :------------------------------------------------- |
| `instance_public_ip`  | The public IP address of the Cloud Critter instance. |
| `instance_id`         | The ID of the Cloud Critter instance.              |
| `security_group_id`   | The ID of the security group created for the Cloud Critter. |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 4.0`
