# Nightly Chrono-Beacon

## Summary
A Terraform module to deploy a highly available, whimsical time synchronization beacon in AWS, providing current UTC time and a philosophical musing.

## Description
In the chaotic aftermath, reliable timekeeping is a luxury. The Nightly Chrono-Beacon provides a simple, resilient web endpoint that echoes the current UTC time and a randomly selected whimsical message, ensuring that even when all else fails, you know *what time it is*. It's built for high availability using AWS Auto Scaling Groups and an Application Load Balancer, making it a steadfast point of temporal reference in an unpredictable world.

## Features
- **Highly Available**: Deploys across multiple Availability Zones using an Auto Scaling Group and Application Load Balancer.
- **Simple API**: Exposes a `/` endpoint returning JSON with current UTC time and a whimsical insight.
- **Whimsical Insights**: Each request includes a randomly selected philosophical message about time.
- **Scalable**: Automatically scales instances based on demand (though a time beacon is unlikely to be heavily loaded).
- **Self-contained**: All necessary infrastructure is provisioned by the module.

## Usage
To use this module, include it in your Terraform configuration and provide the required variables. Ensure you have AWS credentials configured for Terraform.

```terraform
provider "aws" {
  region = "us-east-1"
}

module "chrono_beacon" {
  source = "./src" # Or a Git/S3 path if published

  region          = "us-east-1"
  instance_type   = "t2.micro"
  vpc_id          = "vpc-xxxxxxxxxxxxxxxxx" # Replace with your VPC ID
  subnet_ids      = [
    "subnet-xxxxxxxxxxxxxxxxx", # Replace with your subnet IDs
    "subnet-yyyyyyyyyyyyyyyyy"
  ]
  desired_capacity = 1
  min_size         = 1
  max_size         = 2
  ami_id           = "ami-0abcdef1234567890" # Specify a suitable Amazon Linux 2 AMI for your region
}

output "chrono_beacon_url" {
  value       = module.chrono_beacon.beacon_url
  description = "The URL of the Chrono-Beacon endpoint."
}

output "chrono_beacon_lb_dns" {
  value       = module.chrono_beacon.load_balancer_dns_name
  description = "The DNS name of the Application Load Balancer."
}
```

## Inputs
| Name             | Description                                                              | Type        | Default     | Required |
|------------------|--------------------------------------------------------------------------|-------------|-------------|----------|
| `region`         | AWS region to deploy resources in.                                       | `string`    | n/a         | yes      |
| `instance_type`  | EC2 instance type for the beacon application.                            | `string`    | `t2.micro`  | no       |
| `vpc_id`         | The ID of the VPC where the beacon will be deployed.                     | `string`    | n/a         | yes      |
| `subnet_ids`     | A list of subnet IDs for the Auto Scaling Group and Load Balancer.       | `list(string)` | n/a         | yes      |
| `desired_capacity` | The desired number of EC2 instances in the Auto Scaling Group.           | `number`    | `1`         | no       |
| `min_size`       | The minimum number of EC2 instances in the Auto Scaling Group.           | `number`    | `1`         | no       |
| `max_size`       | The maximum number of EC2 instances in the Auto Scaling Group.           | `number`    | `1`         | no       |
| `ami_id`         | The AMI ID for the EC2 instances (e.g., Amazon Linux 2).                 | `string`    | n/a         | yes      |

## Outputs
| Name                     | Description                                      |
|--------------------------|--------------------------------------------------|
| `beacon_url`             | The full URL of the Chrono-Beacon endpoint.      |
| `load_balancer_dns_name` | The DNS name of the Application Load Balancer.   |

## Tests
To run the module's self-contained tests:

1. Ensure you have Terraform CLI installed.
2. Navigate to the `tests/` directory.
3. Run the test script:
   ```bash
   ./test.sh
   ```

The tests perform a `terraform plan` operation against a dummy configuration, validating that the expected AWS resources are planned without making actual API calls to AWS. This ensures the module's HCL syntax and basic resource definitions are correct.
