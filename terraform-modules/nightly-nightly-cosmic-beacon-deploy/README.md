# Nightly Cosmic Beacon Deployer

This Terraform module deploys an auto-scaling "Cosmic Beacon" on AWS. The beacon is a simple web service that emits whimsical, encouraging messages to the void. It's designed to demonstrate a resilient, scalable infrastructure pattern, automatically adjusting its capacity based on simulated "cosmic distress signals" (CPU utilization).

## Features

*   **Auto-Scaling**: Automatically scales EC2 instances up or down based on CPU load.
*   **Load Balancing**: Distributes incoming requests using an Application Load Balancer (ALB).
*   **Whimsical Messages**: The beacon emits uplifting messages to brighten the cosmic void.
*   **Self-Contained**: Deploys a complete, isolated network and compute environment.

## Usage

1.  **Prerequisites**:
    *   AWS Account configured with credentials (e.g., via `~/.aws/credentials` or environment variables).
    *   Terraform installed.

2.  **Module Input Variables**:
    *   `aws_region`: (string, required) The AWS region to deploy resources in.
    *   `instance_type`: (string, optional, default "t3.micro") EC2 instance type for the beacon.
    *   `min_size`: (number, optional, default 1) Minimum number of beacon instances.
    *   `max_size`: (number, optional, default 3) Maximum number of beacon instances.
    *   `desired_capacity`: (number, optional, default 1) Desired number of beacon instances.
    *   `ami_id`: (string, optional, default "ami-053b0d534c2791404") The AMI ID for the EC2 instances. Defaults to latest Amazon Linux 2023 (us-east-1). **Note**: If using a different region, you must provide an AMI ID valid for that region.

3.  **Deployment**:

    Create a `main.tf` file in your working directory:

    ```terraform
    module "cosmic_beacon" {
      source = "./src" # Or a Git/S3 source if published
      aws_region = "us-east-1"
      instance_type = "t3.small"
      min_size = 1
      max_size = 5
    }

    output "beacon_url" {
      value = module.cosmic_beacon.beacon_url
      description = "The URL of the Cosmic Beacon."
    }
    ```

    Initialize Terraform:
    ```bash
    terraform init
    ```

    Review the plan:
    ```bash
    terraform plan
    ```

    Apply the changes:
    ```bash
    terraform apply
    ```

    After deployment, the `beacon_url` output will provide the URL to access your whimsical beacon.

4.  **Cleanup**:
    To destroy all deployed resources:
    ```bash
    terraform destroy
    ```

## How it Works

The module sets up a VPC, subnets, an ALB, and an Auto Scaling Group. Each EC2 instance launched by the ASG runs a simple Python Flask application. This application serves a random whimsical message on its root path. The ASG is configured with a scaling policy that targets 50% average CPU utilization, simulating a response to "cosmic distress signals" – as load increases, more beacons are launched.

## Testing

The `tests/test_plan.sh` script performs a basic `terraform validate` and `terraform plan` to ensure the module's syntax is correct and a deployment plan can be generated without errors. This is an offline, deterministic check.
