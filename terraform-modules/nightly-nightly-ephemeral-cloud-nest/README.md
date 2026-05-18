# Nightly Ephemeral Cloud Nest

## Summary

The `nightly-ephemeral-cloud-nest` Terraform module provisions a small, isolated, and temporary cloud environment designed for quick testing, development, or ephemeral workloads. It creates a dedicated VPC, a public subnet, a security group, and a basic EC2 instance, all tagged for easy identification and potential automated cleanup.

This "nest" is perfect for spinning up a sandbox for a few hours, running a specific test, or trying out a new tool without cluttering your main cloud infrastructure. It's built with the expectation of being torn down shortly after use.

## Features

*   **Isolated Environment**: Dedicated VPC and subnet.
*   **Basic Compute**: A small EC2 instance (t2.micro) running Amazon Linux 2.
*   **Network Access**: Security group allowing SSH (port 22) and HTTP (port 80) from anywhere.
*   **Ephemeral Tagging**: Resources are tagged with `ephemeral = "true"` and a `ttl` (Time To Live) in hours, facilitating automated cleanup by external tools.
*   **Easy Teardown**: Designed for simple `terraform destroy` when no longer needed.

## Usage

1.  **Prerequisites**:
    *   Terraform CLI installed (version 1.0+ recommended).
    *   AWS CLI configured with credentials that have permissions to create VPCs, subnets, security groups, and EC2 instances.
    *   `jq` installed (for running tests).

2.  **Module Integration**:
    Create a new directory for your project and a `main.tf` file:

    ```terraform
    # main.tf
    provider "aws" {
      region = "us-east-1" # Or your desired region
    }

    module "ephemeral_nest" {
      source = "./path/to/nightly-ephemeral-cloud-nest/src"

      project_name = "my-test-project"
      instance_type = "t2.micro"
      ami_id = "ami-0abcdef1234567890" # Replace with a valid AMI ID for your region (e.g., Amazon Linux 2)
      ttl_hours = 4 # Nest will be tagged to live for 4 hours
      key_name = "my-ssh-key" # Optional: Your EC2 Key Pair name for SSH access
      availability_zone = "us-east-1a" # Specify an AZ in your chosen region
    }

    output "instance_public_ip" {
      value = module.ephemeral_nest.instance_public_ip
      description = "The public IP address of the EC2 instance."
    }

    output "vpc_id" {
      value = module.ephemeral_nest.vpc_id
      description = "The ID of the created VPC."
    }
    ```

    **Note on `ami_id`**: You'll need to find a suitable AMI ID for your chosen AWS region. For Amazon Linux 2, you can often find it via the AWS console or CLI (e.g., `aws ec2 describe-images --owners amazon --filters 'Name=name,Values=amzn2-ami-hvm-*-x86_64-gp2' 'Name=state,Values=available' --query 'sort_by(Images, &CreationDate)[-1].ImageId' --region us-east-1 --output text`).

3.  **Initialize Terraform**:

    ```bash
    terraform init
    ```

4.  **Plan and Apply**:

    ```bash
    terraform plan
    terraform apply --auto-approve
    ```

5.  **Access the Nest**:
    After `apply` completes, you can get the instance's public IP:

    ```bash
    terraform output instance_public_ip
    ```

    Then SSH into your instance (if `key_name` was provided):

    ```bash
    ssh -i ~/.ssh/my-ssh-key.pem ec2-user@$(terraform output -raw instance_public_ip)
    ```

6.  **Destroy the Nest**:
    When you're done, tear down all resources:

    ```bash
    terraform destroy --auto-approve
    ```

    **Automated Cleanup**: The `ephemeral = "true"` and `ttl = "<hours>h"` tags are intended to be used by an external cleanup script or service that periodically scans for and terminates expired ephemeral resources. This module itself does not automatically destroy resources after the TTL expires, but provides the necessary metadata for such a system.

## Module Inputs

| Name                | Description                                  | Type     | Default         | Required |
|---------------------|----------------------------------------------|----------|-----------------|----------|
| `project_name`      | A unique name for the project/environment.   | `string` | `"ephemeral-nest"` | no       |
| `instance_type`     | EC2 instance type.                           | `string` | `"t2.micro"`    | no       |
| `ami_id`            | The AMI ID for the EC2 instance.             | `string` | n/a             | yes      |
| `ttl_hours`         | Time To Live for the resources in hours.     | `number` | `1`             | no       |
| `key_name`          | (Optional) EC2 Key Pair name for SSH access. | `string` | `null`          | no       |
| `vpc_cidr_block`    | CIDR block for the VPC.                      | `string` | `"10.0.0.0/16"` | no       |
| `subnet_cidr_block` | CIDR block for the public subnet.            | `string` | `"10.0.1.0/24"` | no       |
| `availability_zone` | The AWS Availability Zone to deploy resources into. | `string` | `"us-east-1a"` | no       |

## Module Outputs

| Name                 | Description                                  |
|----------------------|----------------------------------------------|
| `vpc_id`             | The ID of the created VPC.                   |
| `subnet_id`          | The ID of the created public subnet.         |
| `security_group_id`  | The ID of the created security group.        |
| `instance_id`        | The ID of the created EC2 instance.          |
| `instance_public_ip` | The public IP address of the EC2 instance.   |
