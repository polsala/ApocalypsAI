# Nightly Whimsical Widget Workshop

This Terraform module provides a minimal, isolated AWS environment designed for quickly deploying and testing small, 'whimsical' microservices or applications. It's perfect for experimenting with new ideas without cluttering existing infrastructure or incurring significant costs.

## Features

*   **Isolated Network**: A dedicated VPC, subnet, and internet gateway.
*   **Basic Compute**: A single EC2 instance (default `t2.micro`) for your widget.
*   **Secure Access**: A security group configured for SSH (port 22) and HTTP (port 80).
*   **Customizable**: Easily adjust instance type, region, and naming.

## Usage

To use this module, include it in your root Terraform configuration (`main.tf`):

```terraform
module "whimsical_workshop" {
  source = "./path/to/nightly-whimsical-widget-workshop/src"

  project_name  = "my-first-whimsical-widget"
  aws_region    = "us-east-1"
  instance_type = "t2.micro"
  ami_id        = "ami-0abcdef1234567890" # Replace with a valid AMI for your region
  ssh_key_name  = "my-ssh-key"          # Optional: provide an existing SSH key pair name
}

output "workshop_public_ip" {
  value = module.whimsical_workshop.public_ip
}

output "workshop_security_group_id" {
  value = module.whimsical_workshop.security_group_id
}
```

### Inputs

| Name               | Description                                                               | Type     | Default           | Required |
| :----------------- | :------------------------------------------------------------------------ | :------- | :---------------- | :------- |
| `project_name`     | A unique name for your whimsical widget, used for resource tagging.       | `string` | `whimsical-widget` | no       |
| `aws_region`       | The AWS region where resources will be provisioned.                       | `string` | `us-east-1`       | no       |
| `instance_type`    | The EC2 instance type for your widget host.                               | `string` | `t2.micro`        | no       |
| `ami_id`           | The AMI ID for the EC2 instance. **Must be a valid AMI for your region.** | `string` | `ami-0abcdef1234567890` | yes      |
| `ssh_key_name`     | (Optional) The name of an existing EC2 key pair for SSH access.           | `string` | `null`            | no       |

### Outputs

| Name                     | Description                                     |
| :----------------------- | :---------------------------------------------- |
| `vpc_id`                 | The ID of the created VPC.                      |
| `public_ip`              | The public IP address of the EC2 instance.      |
| `security_group_id`      | The ID of the security group for the EC2 instance. |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 5.0`

## Development & Testing

To run the automated tests for this module, navigate to the `tests/` directory and execute the `test.sh` script. This will validate the Terraform configuration and attempt to generate a plan without actually provisioning resources.

```bash
cd tests/
bash test.sh
```
