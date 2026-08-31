# Nightly Temporal Resource Replicator

This Terraform module allows you to create "temporal echoes" or shadow replicas of existing AWS EC2 instances. These replicas can be provisioned in different regions, with modified instance types, AMIs, or tags, making them ideal for:

*   **Disaster Recovery Testing**: Simulate recovery by provisioning instances in a secondary region.
*   **Configuration Auditing**: Compare the configuration of the echo with the original to detect drift.
*   **Upgrade/Downgrade Testing**: Test new AMIs or instance types without impacting production.
*   **Ephemeral Test Environments**: Quickly spin up similar instances for development or testing.

## Usage

To use this module, define it in your Terraform configuration and provide the necessary inputs. You will need to configure two AWS providers in your root module: a default one for the source instance's region, and an aliased one (`aws.target`) for the target region where the replica will be created.

```terraform
# Example root module configuration (e.g., main.tf in your calling directory)

# Source region provider
provider "aws" {
  region = "us-east-1" # Region of your source EC2 instance
}

# Target region provider (aliased)
provider "aws" {
  alias  = "target"
  region = "us-west-1" # Region where the echo instance will be created
}

module "ec2_echo" {
  source = "./path/to/nightly-temporal-resource-replicator/src" # Adjust path as needed

  source_instance_id    = "i-0abcdef1234567890" # Replace with your actual instance ID
  target_region         = "us-west-1"
  replica_name_prefix   = "temporal-echo"
  ami_override          = "ami-0abcdef1234567890" # Optional: specify a different AMI
  instance_type_override = "t3.small"             # Optional: specify a different instance type
  tags_to_add = {
    "Environment" = "EchoTest"
    "Purpose"     = "TemporalReplication"
  }
  # subnet_id          = "subnet-0123456789abcdef0" # Optional: specify a target subnet
  # security_group_ids = ["sg-0abcdef1234567890"]    # Optional: specify target security groups
}

output "echo_instance_id" {
  description = "The ID of the created echo EC2 instance."
  value       = module.ec2_echo.echo_instance_id
}

output "echo_instance_public_ip" {
  description = "The public IP of the created echo EC2 instance."
  value       = module.ec2_echo.echo_instance_public_ip
}
```

## Inputs

| Name                     | Description                                                                                                                             | Type          | Default     | Required |
| :----------------------- | :-------------------------------------------------------------------------------------------------------------------------------------- | :------------ | :---------- | :------- |
| `source_instance_id`     | The ID of the existing EC2 instance to replicate.                                                                                       | `string`      | `n/a`       | yes      |
| `target_region`          | The AWS region where the replica instance will be created.                                                                              | `string`      | `n/a`       | yes      |
| `replica_name_prefix`    | A prefix for the name tag of the replicated instance.                                                                                   | `string`      | `"echo"`    | no       |
| `ami_override`           | Optional: Override the AMI ID of the source instance.                                                                                   | `string`      | `null`      | no       |
| `instance_type_override` | Optional: Override the instance type of the source instance.                                                                            | `string`      | `null`      | no       |
| `tags_to_add`            | Optional: A map of additional tags to apply to the replicated instance. These tags will be merged with and can override source instance tags. | `map(string)` | `{}`        | no       |
| `subnet_id`              | Optional: The ID of the subnet to launch the instance into. If not provided, Terraform will attempt to use the default subnet in the target region. | `string`      | `null`      | no       |
| `security_group_ids`     | Optional: A list of security group IDs to associate with the instance. If not provided, Terraform will attempt to use the default security group in the target region. | `list(string)` | `[]`        | no       |

## Outputs

| Name                      | Description                                 |
| :------------------------ | :------------------------------------------ |
| `echo_instance_id`        | The ID of the created echo EC2 instance.    |
| `echo_instance_public_ip` | The public IP of the created echo EC2 instance. |
