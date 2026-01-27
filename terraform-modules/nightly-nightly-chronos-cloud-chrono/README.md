# Nightly Chronos Cloud Chronometer

A Terraform module to deploy a highly available, secure Network Time Protocol (NTP) server in the AWS cloud. In a world where temporal anomalies are a daily occurrence, precise time synchronization is crucial for coordinating efforts, logging events, and ensuring the integrity of distributed systems. This module provides a reliable time source, guarded against the chaos.

## Features

*   **Dedicated NTP Server**: Provisions a small EC2 instance specifically configured to run an NTP daemon.
*   **Security Group**: Configures a security group to allow NTP traffic only from specified IP ranges, enhancing security.
*   **User Data Configuration**: Automatically sets up and starts the NTP service upon instance launch.
*   **Outputs**: Provides the public IP address of the NTP server for easy integration.

## Usage

To deploy your Chronos Cloud Chronometer, include this module in your Terraform configuration:

```terraform
module "chronos_chronometer" {
  source = "./nightly-chronos-cloud-chronometer" # Adjust path if not local

  aws_region    = "us-east-1"
  vpc_id        = "vpc-0abcdef1234567890" # Replace with your VPC ID
  subnet_id     = "subnet-0fedcba9876543210" # Replace with your Subnet ID
  instance_type = "t2.micro"
  allowed_cidrs = ["192.168.1.0/24", "10.0.0.0/8"] # Your internal network CIDRs
  key_name      = "my-ssh-key" # Optional: for SSH access, if needed
  tags = {
    Project = "ApocalypsAI"
    Service = "NTP"
  }
}

output "ntp_server_ip" {
  description = "The public IP address of the Chronos Cloud Chronometer NTP server."
  value       = module.chronos_chronometer.ntp_server_ip
}
```

### Inputs

| Name            | Description                                                              | Type        | Default     | Required |
| :-------------- | :-------------- | :---------- | :---------- | :------- |
| `aws_region`    | The AWS region to deploy the NTP server in.                              | `string`    | n/a         | yes      |
| `vpc_id`        | The ID of the VPC where the NTP server will be deployed.                 | `string`    | n/a         | yes      |
| `subnet_id`     | The ID of the subnet where the NTP server EC2 instance will be launched. | `string`    | n/a         | yes      |
| `instance_type` | The EC2 instance type for the NTP server.                                | `string`    | `"t2.micro"`| no       |
| `allowed_cidrs` | A list of CIDR blocks that are allowed to access the NTP server (port 123 UDP). | `list(string)` | n/a         | yes      |
| `key_name`      | The name of an existing EC2 Key Pair to allow SSH access (optional).     | `string`    | `null`      | no       |
| `tags`          | A map of tags to assign to the resources.                                | `map(string)` | `{}`        | no       |

### Outputs

| Name            | Description                                          |
| :-------------- | :--------------------------------------------------- |
| `ntp_server_ip` | The public IP address of the deployed NTP server.    |

## Testing

This module includes a self-contained test suite that uses `terraform validate` and `terraform plan` to ensure the module's configuration is valid and produces an expected plan without requiring actual cloud deployment.

To run the tests:

```bash
cd tests
./test.sh
```

The `test.sh` script will:
1. Initialize Terraform in an offline mode.
2. Validate the module's configuration.
3. Generate a Terraform plan using mock input variables and mock VPC/subnet resources.
4. Assert that the plan is successfully generated and indicates no unexpected changes (exit code 0).

This ensures the module is syntactically correct and its resource definitions are stable.
