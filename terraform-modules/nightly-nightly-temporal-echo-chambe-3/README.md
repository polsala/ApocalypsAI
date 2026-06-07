# Nightly Temporal Echo Chamber (Terraform Module)

## Summary
This Terraform module creates an isolated, ephemeral AWS cloud environment, affectionately dubbed a "Temporal Echo Chamber." It's designed for developers, testers, or curious minds who need a safe, self-contained space to experiment with time-sensitive applications, test infrastructure changes, or simply play around without impacting production resources. Spin it up, run your experiments, and tear it down – leaving no trace.

## Features
-   **Isolated Network:** A dedicated Virtual Private Cloud (VPC) and subnet.
-   **Basic Compute:** A single EC2 instance for running your applications or scripts.
-   **Internet Access:** Configured with an Internet Gateway and route table for outbound connectivity.
-   **SSH Access:** A security group allowing SSH from a specified CIDR block.
-   **Ephemeral:** Easily provisioned and destroyed, perfect for temporary use cases.

## Usage

1.  **Prerequisites:**
    -   [Terraform](https://www.terraform.io/downloads.html) installed.
    -   AWS CLI configured with credentials that have permissions to create VPCs, EC2 instances, etc.

2.  **Module Integration:**
    Create a `main.tf` file in your project and reference this module:

    ```terraform
    module "temporal_echo_chamber" {
      source = "./path/to/nightly-temporal-echo-chamber-tf/src"

      region        = "us-east-1"
      instance_type = "t2.micro"
      ami_id        = "ami-0abcdef1234567890" # Replace with a valid AMI for your region
      key_name      = "my-ssh-key"          # Replace with an existing EC2 Key Pair name
      vpc_cidr      = "10.0.0.0/16"
      subnet_cidr   = "10.0.1.0/24"
      allowed_ssh_cidr = "0.0.0.0/0"       # WARNING: Restrict this to your IP for security!

      tags = {
        Project     = "ApocalypsAI"
        Environment = "TemporalEchoChamber"
      }
    }

    output "instance_public_ip" {
      value       = module.temporal_echo_chamber.instance_public_ip
      description = "The public IP address of the EC2 instance."
    }

    output "vpc_id" {
      value       = module.temporal_echo_chamber.vpc_id
      description = "The ID of the created VPC."
    }
    ```

    **Important:** Replace `ami_id` and `key_name` with values appropriate for your AWS region and setup. For `ami_id`, you can find current Amazon Linux 2 AMIs in the AWS console or via AWS CLI (e.g., `aws ec2 describe-images --owners amazon --filters 'Name=name,Values=amzn2-ami-hvm-*-x86_64-gp2' 'Name=state,Values=available' --query 'sort_by(Images, &CreationDate)[-1].ImageId'`).

3.  **Initialize Terraform:**
    ```bash
    terraform init
    ```

4.  **Plan and Apply:**
    Review the plan before applying:
    ```bash
    terraform plan
    terraform apply
    ```

5.  **Access the Instance:**
    Once applied, you can SSH into your instance using the outputted public IP:
    ```bash
    ssh -i ~/.ssh/my-ssh-key.pem ec2-user@$(terraform output -raw instance_public_ip)
    ```

6.  **Destroy the Echo Chamber:**
    When you're done experimenting, clean up all resources:
    ```bash
    terraform destroy
    ```

## Inputs

| Name             | Description                                     | Type     | Default     | Required |
|------------------|-------------------------------------------------|----------|-------------|----------|
| `region`         | AWS region to deploy resources into.            | `string` | `"us-east-1"` | yes      |
| `instance_type`  | EC2 instance type.                              | `string` | `"t2.micro"`| yes      |
| `ami_id`         | AMI ID for the EC2 instance.                    | `string` | n/a         | yes      |
| `key_name`       | Name of an existing EC2 Key Pair for SSH access.| `string` | n/a         | yes      |
| `vpc_cidr`       | CIDR block for the VPC.                         | `string` | `"10.0.0.0/16"` | yes      |
| `subnet_cidr`    | CIDR block for the public subnet.               | `string` | `"10.0.1.0/24"` | yes      |
| `allowed_ssh_cidr` | CIDR block allowed to SSH into the EC2 instance. | `string` | `"0.0.0.0/0"` | yes      |
| `tags`           | A map of tags to apply to all resources.        | `map(string)` | `{}`        | no       |

## Outputs

| Name                 | Description                                  |
|----------------------|----------------------------------------------|
| `vpc_id`             | The ID of the created VPC.                   |
| `subnet_id`          | The ID of the created public subnet.         |
| `instance_public_ip` | The public IP address of the EC2 instance.   |
| `instance_id`        | The ID of the created EC2 instance.          |
| `security_group_id`  | The ID of the created security group.        |

## Testing

To run the tests, navigate to the module's root directory and execute:

```bash
chmod +x tests/test_plan.sh
./tests/test_plan.sh
```

This script performs a `terraform plan` and verifies the expected resources are part of the plan, ensuring the module's structure is correct without actual AWS deployment.
