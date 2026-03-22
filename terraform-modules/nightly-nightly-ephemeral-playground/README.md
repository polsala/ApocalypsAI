# Nightly Ephemeral Playground

## Summary
This Terraform module provisions a temporary, isolated AWS EC2 instance along with its necessary networking components (VPC, subnet, security group, etc.). The instance is tagged with `EphemeralPlayground: true` and a `DestroyAfter` timestamp, indicating when it should be considered for automatic cleanup by a separate (hypothetical) ApocalypsAI cleanup agent. It's perfect for quick experiments, testing, or just having a digital sandbox that won't linger forever.

## Whimsical Touch
The instance is given a whimsical, randomly generated name to make your ephemeral adventures a little more delightful. It also comes with a `DestroyAfter` tag, a gentle reminder from the ApocalypsAI that even the most fun playgrounds eventually need tidying up.

## How it Works
1.  **Isolation**: Creates a dedicated AWS VPC and subnet to keep your playground separate from other resources.
2.  **Access**: Sets up an Internet Gateway, route table, and a security group allowing SSH access (port 22) from anywhere (for simplicity; restrict in production).
3.  **Instance**: Launches an EC2 instance based on your specified AMI and instance type.
4.  **Key Pair**: Uses an existing or newly created AWS Key Pair for SSH access.
5.  **Self-Tagging**: Automatically applies `EphemeralPlayground: true` and `DestroyAfter` tags to the instance, making it discoverable for automated cleanup processes.

## Prerequisites
*   [Terraform](https://www.terraform.io/downloads.html) installed.
*   [AWS CLI](https://aws.amazon.com/cli/) configured with credentials that have permissions to create VPCs, EC2 instances, security groups, and key pairs.
*   An SSH public key file (`.pub`) to be used for accessing the EC2 instance.

## Usage
1.  **Create a `main.tf` file** in a new directory and reference this module:

    ```terraform
    module "ephemeral_playground" {
      source = "./src" # Path to this module's 'src' directory

      region          = "us-east-1" # Or your desired region
      instance_type   = "t2.micro"
      ami_id          = "ami-053b0d53c279acc90" # Example: Amazon Linux 2 AMI (HVM) for us-east-1
      key_name        = "my-ssh-key" # Name of your AWS Key Pair
      public_key_path = "~/.ssh/id_rsa.pub" # Path to your public key file
      destroy_after_hours = 48 # Tag for destruction after 48 hours
    }

    output "playground_ip" {
      value = module.ephemeral_playground.public_ip
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

4.  **Apply the configuration** to provision the playground:

    ```bash
    terraform apply
    ```

5.  **Access your playground**: Use the output `playground_ip` to SSH into your instance:

    ```bash
    ssh -i ~/.ssh/id_rsa ec2-user@<playground_ip>
    ```

6.  **Destroy the playground**: When you're done playing, clean up your resources:

    ```bash
    terraform destroy
    ```

## Inputs
| Name                | Description                                                              | Type   | Default             | Required |
|---------------------|--------------------------------------------------------------------------|--------|---------------------|----------|
| `region`            | AWS region to deploy resources.                                          | `string` | `"us-east-1"`       | no       |
| `instance_type`     | EC2 instance type for the playground.                                    | `string` | `"t2.micro"`        | no       |
| `ami_id`            | AMI ID for the EC2 instance (e.g., Amazon Linux 2 HVM).                  | `string` | `"ami-053b0d53c279acc90"` | no       |
| `key_name`          | Name of the AWS Key Pair to use for SSH access.                          | `string` |                     | yes      |
| `public_key_path`   | Path to the public key file (.pub) to create the AWS Key Pair.           | `string` |                     | yes      |
| `destroy_after_hours` | Number of hours after which the playground should be considered for destruction. | `number` | `24`                | no       |

## Outputs
| Name              | Description                                                |
|-------------------|------------------------------------------------------------|
| `public_ip`       | Public IP address of the ephemeral playground instance.    |
| `instance_id`     | ID of the ephemeral playground instance.                   |
| `destroy_after_tag` | Timestamp when the instance is tagged for destruction.     |
