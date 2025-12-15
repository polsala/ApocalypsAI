# Nightly Ephemeral Garden Terraform Module

This Terraform module provisions a collection of cloud resources designed for ephemerality, making them ideal for development, testing, and temporary environments. It sets up an EC2 instance, an S3 bucket, and an RDS database with configurations that facilitate easy creation, use, and rapid deletion.

## Features

-   **Ephemeral EC2 Instance**: Configured to allow API termination and terminate on instance-initiated shutdown.
-   **Ephemeral S3 Bucket**: Includes a lifecycle rule to automatically expire objects after a short period (default: 7 days) and disables versioning by default.
-   **Ephemeral RDS Database**: Configured to skip final snapshots and disable deletion protection, allowing for quick teardown.
-   **Customizable**: All core resource properties are exposed as variables for flexible configuration.

## Usage

To use this module, include it in your Terraform configuration and provide the necessary variables. Ensure your AWS provider is configured.

```terraform
provider "aws" {
  region = "us-east-1"
}

module "my_ephemeral_garden" {
  source = "./path/to/nightly-ephemeral-garden" # Adjust path as needed

  name_prefix                 = "my-dev-env"
  ami_id                      = "ami-0abcdef1234567890" # Replace with a valid AMI for your region
  instance_type               = "t3.micro"
  subnet_id                   = "subnet-0123456789abcdef0" # Replace with your subnet ID
  vpc_security_group_ids      = ["sg-0abcdef1234567890"] # Replace with your security group ID
  associate_public_ip_address = false

  s3_object_expiration_days   = 3 # Objects expire after 3 days

  db_allocated_storage        = 20
  db_engine                   = "mysql"
  db_engine_version           = "5.7"
  db_instance_class           = "db.t3.micro"
  db_name                     = "devdb"
  db_username                 = "devuser"
  db_password                 = "SuperSecretDevPass123!"
  db_subnet_group_name        = "my-db-subnet-group" # Replace with your DB subnet group name
}

output "ec2_id" {
  value = module.my_ephemeral_garden.ec2_instance_id
}

output "s3_bucket_name" {
  value = module.my_ephemeral_garden.s3_bucket_id
}

output "rds_endpoint" {
  value = module.my_ephemeral_garden.rds_instance_address
}
```

## Inputs

| Name                        | Description                                                                 | Type        | Default                               | Required |
|-----------------------------|-----------------------------------------------------------------------------|-------------|---------------------------------------|----------|
| `name_prefix`               | A prefix for all resource names to ensure uniqueness and identification.    | `string`    | `"apocalypsai"`                       | no       |
| `ami_id`                    | The AMI ID for the EC2 instance.                                            | `string`    | `"ami-0abcdef1234567890"`             | no       |
| `instance_type`             | The type of EC2 instance to launch.                                         | `string`    | `"t3.micro"`                          | no       |
| `subnet_id`                 | The ID of the subnet to launch the EC2 instance into.                       | `string`    | `"subnet-0123456789abcdef0"`          | no       |
| `vpc_security_group_ids`    | A list of security group IDs to associate with the EC2 instance and RDS.    | `list(string)` | `["sg-0abcdef1234567890"]`            | no       |
| `associate_public_ip_address` | Whether to associate a public IP address with the EC2 instance.             | `bool`      | `false`                               | no       |
| `s3_object_expiration_days` | Number of days after which S3 objects will expire.                          | `number`    | `7`                                   | no       |
| `db_allocated_storage`      | The allocated storage in gigabytes for the DB instance.                     | `number`    | `20`                                  | no       |
| `db_engine`                 | The database engine to use.                                                 | `string`    | `"mysql"`                             | no       |
| `db_engine_version`         | The database engine version.                                                | `string`    | `"5.7"`                               | no       |
| `db_instance_class`         | The instance type of the RDS database.                                      | `string`    | `"db.t3.micro"`                       | no       |
| `db_name`                   | The name of the database to create.                                         | `string`    | `"ephemeraldb"`                       | no       |
| `db_username`               | The master username for the database.                                       | `string`    | `"admin"`                             | no       |
| `db_password`               | The master password for the database. **Sensitive.**                        | `string`    | `"Password123!"`                      | no       |
| `db_subnet_group_name`      | The name of the DB subnet group to associate with the RDS instance.         | `string`    | `"default-vpc-0123456789abcdef0"`     | no       |

## Outputs

| Name                   | Description                                  |
|------------------------|----------------------------------------------|
| `ec2_instance_id`      | The ID of the provisioned EC2 instance.      |
| `s3_bucket_id`         | The ID of the provisioned S3 bucket.         |
| `rds_instance_address` | The address of the provisioned RDS instance. |

## Testing

Refer to the `tests/test.sh` script for how to run offline, deterministic tests for this module. It uses `terraform validate` and `terraform plan` to assert the ephemeral characteristics without deploying actual cloud resources.
