# Nightly Ephemeral Cloud Outpost

A Terraform module to provision a temporary, secure AWS EC2 instance for ephemeral operations.

## Overview

In the ever-shifting landscape of the post-apocalyptic digital realm, sometimes you need a quick, secure, and disposable base of operations. The `Nightly Ephemeral Cloud Outpost` module allows you to rapidly deploy a minimal AWS EC2 instance, complete with a dedicated security group and key pair, designed for short-term tasks like data processing, secure communication relays, or temporary computation. Once its mission is complete, it can be swiftly dismantled, leaving no trace.

Think of it as a digital pop-up shelter – robust for its brief existence, then gone with the wind.

## Features

*   **Ephemeral by Design**: Easily provision and de-provision a single EC2 instance.
*   **Secure**: Automatically creates a dedicated security group with configurable ingress rules.
*   **Key Pair Management**: Generates a new SSH key pair for secure access.
*   **Configurable**: Customize instance type, AMI, and region.

## Usage

1.  **Prerequisites**:
    *   Terraform installed (v1.0.0+)
    *   AWS CLI configured with appropriate credentials and default region.

2.  **Module Integration**:
    Create a `main.tf` file in your root Terraform configuration:

    ```terraform
    module "ephemeral_outpost" {
      source = "./nightly-ephemeral-cloud-outpost/src" # Adjust path if necessary

      instance_name = "apocalypsai-outpost-001"
      instance_type = "t2.micro"
      ami_id        = "ami-0abcdef1234567890" # Replace with a valid AMI for your region (e.g., Amazon Linux 2)
      key_name      = "apocalypsai-outpost-key"
      ingress_ports = [22, 80] # Allow SSH and HTTP access
      region        = "us-east-1" # Specify your desired AWS region
    }

    output "outpost_public_ip" {
      description = "The public IP address of the ephemeral outpost."
      value       = module.ephemeral_outpost.public_ip
    }

    output "outpost_instance_id" {
      description = "The ID of the ephemeral outpost EC2 instance."
      value       = module.ephemeral_outpost.instance_id
    }

    output "outpost_private_key_pem" {
      description = "The private key in PEM format for SSH access. **Handle with care!**"
      value       = module.ephemeral_outpost.private_key_pem
      sensitive   = true
    }
    ```

    **Important**: Replace `ami-0abcdef1234567890` with a valid AMI ID for your chosen region. You can find AMIs using the AWS console or CLI (e.g., `aws ec2 describe-images --owners amazon --filters "Name=name,Values=amzn2-ami-hvm-*-x86_64-gp2" --query "Images[0].ImageId"`).

3.  **Initialize Terraform**:
    ```bash
    terraform init
    ```

4.  **Plan the Deployment**:
    ```bash
    terraform plan
    ```

5.  **Apply the Configuration**:
    ```bash
    terraform apply
    ```
    This will provision the EC2 instance and output the public IP and the private key. Save the private key securely!

6.  **Access the Outpost**:
    ```bash
    chmod 400 <path-to-saved-private-key.pem>
    ssh -i <path-to-saved-private-key.pem> ec2-user@<outpost_public_ip>
    ```

7.  **Destroy the Outpost**:
    When the mission is complete, tear down the outpost:
    ```bash
    terraform destroy
    ```

## Inputs

| Name            | Description                                   | Type     | Default     | Required |
| :-------------- | :-------------------------------------------- | :------- | :---------- | :------- |
| `instance_name` | Name tag for the EC2 instance.                | `string` | `"ephemeral-outpost"` | no       |
| `instance_type` | The EC2 instance type.                        | `string` | `"t2.micro"` | no       |
| `ami_id`        | The AMI ID for the EC2 instance.              | `string` | n/a         | yes      |
| `key_name`      | The name for the generated SSH key pair.      | `string` | `"ephemeral-key"` | no       |
| `ingress_ports` | List of ports to allow ingress from anywhere. | `list(number)` | `[22]`      | no       |
| `region`        | AWS region to deploy resources into.          | `string` | `"us-east-1"` | no       |

## Outputs

| Name                | Description                                     |
| :------------------ | :---------------------------------------------- |
| `instance_id`       | The ID of the provisioned EC2 instance.         |
| `public_ip`         | The public IP address of the EC2 instance.      |
| `private_key_pem`   | The generated private key in PEM format. **Handle with extreme care!** |
| `security_group_id` | The ID of the created security group.           |

## Testing

The module includes Terraform native tests (`.tftest.hcl`) that use `mock_provider` to simulate AWS resources, ensuring the module's logic is sound without actual cloud deployments.

To run tests:
```bash
terraform test
```
