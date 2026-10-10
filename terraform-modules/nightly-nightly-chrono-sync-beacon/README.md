# Nightly Chrono-Sync Beacon

## Summary
This Terraform module deploys a highly available Network Time Protocol (NTP) server, powered by `chrony`, on an AWS EC2 instance. It ensures precise temporal synchronization across your distributed infrastructure, a critical component for logging, security, and distributed systems in any era, especially the post-apocalyptic one.

## Features
- Deploys an EC2 instance configured as an NTP server using `chrony`.
- Configures a security group to allow NTP (UDP 123) traffic.
- Uses `user_data` to automate `chrony` installation and setup.
- Includes a Terraform `check` block for validating instance types.

## Usage
To deploy your Chrono-Sync Beacon, you'll need an existing AWS VPC and subnet. Create a `main.tf` file in your root Terraform configuration and reference this module:

```terraform
module "chrono_sync_beacon" {
  source = "./path/to/nightly-chrono-sync-beacon/src"

  aws_region    = "us-east-1"
  vpc_id        = "vpc-xxxxxxxxxxxxxxxxx" # REPLACE with your VPC ID
  subnet_id     = "subnet-xxxxxxxxxxxxxxxxx" # REPLACE with your Subnet ID
  instance_type = "t2.micro"
  ami_id        = "ami-053b0d53ed77771ad" # Amazon Linux 2 AMI (HVM) - Kernel 5.10, SSD Volume Type, us-east-1
  key_name      = null # Optional: "your-ssh-key-name"
  environment   = "production"
}

output "beacon_public_ip" {
  value = module.chrono_sync_beacon.public_ip
}

output "beacon_public_dns" {
  value = module.chrono_sync_beacon.public_dns
}
```

Then, run the standard Terraform commands:

```bash
terraform init
terraform plan
terraform apply
```

## Inputs
| Name          | Description                                                              | Type     | Default                         | Required |
|---------------|--------------------------------------------------------------------------|----------|---------------------------------|----------|
| `aws_region`  | AWS region to deploy resources.                                          | `string` | `"us-east-1"`                   | no       |
| `vpc_id`      | The ID of the VPC where the Chrono-Sync Beacon will be deployed.         | `string` | n/a                             | yes      |
| `subnet_id`   | The ID of the subnet where the Chrono-Sync Beacon EC2 instance will be launched. | `string` | n/a                             | yes      |
| `instance_type`| The EC2 instance type for the Chrono-Sync Beacon.                        | `string` | `"t2.micro"`                    | no       |
| `ami_id`      | The AMI ID for the EC2 instance. Must be Amazon Linux 2 compatible.      | `string` | `"ami-053b0d53ed77771ad"`       | no       |
| `key_name`    | The name of the EC2 Key Pair to allow SSH access to the instance (optional). | `string` | `null`                          | no       |
| `environment` | A tag to identify the environment (e.g., 'dev', 'prod').                 | `string` | `"default"`                     | no       |

## Outputs
| Name                | Description                                        |
|---------------------|----------------------------------------------------|
| `public_ip`         | The public IP address of the Chrono-Sync Beacon.   |
| `public_dns`        | The public DNS name of the Chrono-Sync Beacon.     |
| `security_group_id` | The ID of the security group created for the Chrono-Sync Beacon. |

## Testing
To run the module's self-contained tests, navigate to the `tests/` directory and execute `test.sh`:

```bash
cd nightly-chrono-sync-beacon/tests
./test.sh
```
