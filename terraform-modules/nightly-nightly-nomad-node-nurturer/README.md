# Nightly Nomad Node Nurturer

For those moments when your data-carrying pigeon gets intercepted by a rogue drone, and you need a new relay, *fast*! The `nightly-nomad-node-nurturer` is a Terraform module designed to provision a self-healing, ephemeral compute node in the cloud. It's perfect for temporary data processing, communication relays, or any task requiring a resilient, short-lived server in the ever-shifting wasteland.

This module leverages AWS Auto Scaling Groups to ensure that if your node unexpectedly vanishes (perhaps a rogue AI decided it needed the compute power more), a new one will automatically spring up in its place, ready to continue its vital work.

## Features

*   **Self-Healing**: Automatically replaces instances that fail or are terminated.
*   **Ephemeral**: Designed for temporary workloads, easy to provision and de-provision.
*   **Customizable**: Configure instance type, AMI, security groups, and more.
*   **Secure**: Integrates with existing VPC security groups and SSH key pairs.

## Usage

To use this module, include it in your Terraform configuration and provide the necessary variables.

### Prerequisites

*   Terraform installed (v1.0+)
*   AWS CLI configured with appropriate credentials and default region.
*   An existing AWS VPC, subnets, and security groups.
*   An existing EC2 Key Pair for SSH access.

### Example `main.tf`

```terraform
provider "aws" {
  region = "us-east-1"
}

module "nomad_node" {
  source = "./nightly-nomad-node-nurturer"

  name_prefix           = "apocalypsai-nomad-node"
  region                = "us-east-1"
  ami_id                = "ami-0abcdef1234567890" # Replace with a valid AMI ID for your region
  instance_type         = "t3.micro"
  key_name              = "my-ssh-key"        # Replace with your EC2 Key Pair name
  vpc_security_group_ids = ["sg-0123456789abcdef0"]
  subnet_ids            = ["subnet-0fedcba9876543210", "subnet-0123456789abcdef"]
  min_size              = 1
  max_size              = 1
  desired_capacity      = 1

  tags = {
    Project = "ApocalypsAI"
    Purpose = "NomadNode"
  }
}

output "nomad_node_asg_name" {
  description = "The name of the Auto Scaling Group for the Nomad Node."
  value       = module.nomad_node.asg_name
}

output "nomad_node_launch_template_id" {
  description = "The ID of the Launch Template used by the Nomad Node."
  value       = module.nomad_node.launch_template_id
}
```

### Running Terraform

1.  **Initialize Terraform**: Navigate to your configuration directory and run:
    ```bash
    terraform init
    ```
2.  **Plan the deployment**: Review the changes Terraform will make:
    ```bash
    terraform plan
    ```
3.  **Apply the changes**: Deploy the Nomad Node:
    ```bash
    terraform apply
    ```

## Module Inputs

| Name                     | Description                                                              | Type        | Default | Required |
| :----------------------- | :----------------------------------------------------------------------- | :---------- | :------ | :------- |
| `name_prefix`            | A prefix for naming all resources created by the module.                 | `string`    | `"nomad-node"` | no       |
| `region`                 | The AWS region to deploy resources in.                                   | `string`    | n/a     | yes      |
| `ami_id`                 | The ID of the Amazon Machine Image (AMI) to use for the instances.       | `string`    | n/a     | yes      |
| `instance_type`          | The EC2 instance type to use (e.g., `t3.micro`).                         | `string`    | `"t3.micro"` | no       |
| `key_name`               | The name of the EC2 Key Pair for SSH access.                             | `string`    | n/a     | yes      |
| `vpc_security_group_ids` | A list of security group IDs to associate with the instances.            | `list(string)` | n/a     | yes      |
| `subnet_ids`             | A list of subnet IDs where the instances will be launched.               | `list(string)` | n/a     | yes      |
| `min_size`               | The minimum number of instances in the Auto Scaling Group.               | `number`    | `1`     | no       |
| `max_size`               | The maximum number of instances in the Auto Scaling Group.               | `number`    | `1`     | no       |
| `desired_capacity`       | The desired number of instances in the Auto Scaling Group.               | `number`    | `1`     | no       |
| `user_data`              | User data to provide when launching the instances.                       | `string`    | `null`  | no       |
| `tags`                   | A map of tags to apply to all resources created by the module.           | `map(string)` | `{}`    | no       |

## Module Outputs

| Name                      | Description                                     |
| :------------------------ | :---------------------------------------------- |
| `asg_name`                | The name of the created Auto Scaling Group.     |
| `launch_template_id`      | The ID of the created Launch Template.          |
| `launch_template_version` | The version of the created Launch Template.     |

## Contributing

Contributions are welcome! If you have ideas for improving the Nomad Node Nurturer, please open an issue or submit a pull request.
