# Nightly Temporal Beacon

This Terraform module deploys a highly available, static web beacon on AWS. It's designed to signal presence and provide a simple, resilient endpoint, even across the most turbulent temporal distortions. Think of it as a digital lighthouse in the digital wasteland.

## Features

*   **Highly Available:** Deploys across multiple Availability Zones using an Auto Scaling Group and Application Load Balancer.
*   **Simple & Static:** Serves a basic Nginx page with a customizable beacon message and a dynamic timestamp.
*   **Configurable:** Easily adjust instance types, capacity, and the beacon message.

## Usage

To use this module, include it in your Terraform configuration and provide the required inputs. Ensure you have AWS credentials configured.

```terraform
module "temporal_beacon" {
  source = "./modules/nightly-temporal-beacon" # Adjust path if not using local module

  aws_region          = "us-east-1"
  vpc_id              = "vpc-0123456789abcdef0"
  public_subnet_ids   = [
    "subnet-0abcdef1234567890a",
    "subnet-0abcdef1234567890b"
  ]
  instance_type       = "t3.micro"
  desired_capacity    = 2
  beacon_message      = "ApocalypsAI Temporal Beacon Online!"
}

output "beacon_url" {
  value = module.temporal_beacon.alb_dns_name
  description = "The DNS name of the Temporal Beacon's Application Load Balancer."
}
```

## Inputs

| Name                | Description                                                               | Type          | Default       | Required |
|---------------------|---------------------------------------------------------------------------|---------------|---------------|----------|
| `aws_region`        | The AWS region to deploy resources in.                                    | `string`      | `"us-east-1"` | yes      |
| `vpc_id`            | The ID of the VPC where the beacon will be deployed.                      | `string`      | n/a           | yes      |
| `public_subnet_ids` | A list of public subnet IDs (at least two for HA) for the ALB and EC2s. | `list(string)`| n/a           | yes      |
| `instance_type`     | The EC2 instance type for the beacon servers.                             | `string`      | `"t2.micro"`  | no       |
| `desired_capacity`  | The desired number of beacon instances in the Auto Scaling Group.         | `number`      | `2`           | no       |
| `beacon_message`    | The whimsical message to display on the beacon's web page.                | `string`      | `"Temporal Beacon Active!"` | no |

## Outputs

| Name           | Description                                                 |
|----------------|-------------------------------------------------------------|
| `alb_dns_name` | The DNS name of the Application Load Balancer for the beacon. |

## Testing

To run the automated tests, navigate to the `tests/` directory and execute the `test.sh` script. This script performs an offline `terraform plan` and `terraform output` to validate the module's syntax and output structure without deploying actual resources.

```bash
cd tests/
./test.sh
```
