# Nightly Wasteland Watchtower

A Terraform module to provision a minimal "watchtower" in AWS, consisting of a single EC2 instance and an associated security group. This instance can be used as a base for deploying monitoring agents, log collectors, or simple web dashboards to keep an eye on your digital infrastructure.

## Features

*   Provisions an AWS EC2 instance.
*   Creates a security group allowing SSH (port 22) and HTTP (port 80) access.
*   Outputs the public IP and DNS of the instance.

## Usage

1.  **Configure AWS Credentials**: Ensure your AWS credentials are configured (e.g., via `~/.aws/credentials`, environment variables, or IAM roles).

2.  **Create a `main.tf` file (or similar) in your project**:

    ```terraform
    module "watchtower" {
      source        = "./path/to/this/module/src"
      region        = "us-east-1" # Or your desired AWS region
      ami_id        = "ami-0abcdef1234567890" # Replace with a valid AMI ID for your region (e.g., Amazon Linux 2)
      instance_type = "t2.micro"
      key_name      = "your-ssh-key-name" # Replace with an existing EC2 Key Pair name
    }

    output "watchtower_ip" {
      value = module.watchtower.watchtower_public_ip
    }
    ```

3.  **Initialize Terraform**: Navigate to your project directory and run:

    ```bash
    terraform init
    ```

4.  **Review the Plan**: See what Terraform will do:

    ```bash
    terraform plan
    ```

5.  **Apply the Configuration**: Deploy the watchtower:

    ```bash
    terraform apply
    ```

    Confirm with `yes` when prompted.

## Inputs

*   `region` (string, optional): AWS region to deploy resources. Default: `us-east-1`.
*   `ami_id` (string, required): AMI ID for the EC2 instance. **You must provide a valid AMI ID for your chosen region.**
*   `instance_type` (string, optional): EC2 instance type. Default: `t2.micro`.
*   `key_name` (string, required): Name of the EC2 Key Pair to allow SSH access. **You must provide an existing key pair name.**

## Outputs

*   `watchtower_public_ip`: The public IP address of the Watchtower EC2 instance.
*   `watchtower_public_dns`: The public DNS name of the Watchtower EC2 instance.
*   `watchtower_security_group_id`: The ID of the security group attached to the Watchtower.

## Testing

The module includes an offline test script (`tests/test_plan.sh`) that uses `terraform validate` and `terraform plan` to ensure the module's syntax is correct and the planned resources match expectations, without deploying actual cloud infrastructure. This requires `terraform` and `jq` to be installed.

To run the tests:

```bash
./tests/test_plan.sh
```
