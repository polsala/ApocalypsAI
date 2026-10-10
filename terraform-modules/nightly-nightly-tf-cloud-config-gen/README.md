Terraform Cloud Configuration Generator
=======================================

This module provides a foundational Terraform configuration for setting up basic cloud resources in a cloud-agnostic manner. It focuses on creating a simple network infrastructure that can be adapted for various cloud providers.

## Features

*   Generates a basic VPC/Network.
*   Creates a default subnet.
*   Outputs essential network identifiers.

## Usage

To use this module, you would typically include it in your main Terraform configuration like so:

```hcl
module "cloud_infra" {
  source = "./path/to/this/module"

  # Optional: Override default variables
  vpc_cidr_block = "10.0.0.0/16"
  subnet_cidr_block = "10.0.1.0/24"
}

output "vpc_id" {
  description = "The ID of the created VPC."
  value       = module.cloud_infra.vpc_id
}

output "subnet_id" {
  description = "The ID of the created subnet."
  value       = module.cloud_infra.subnet_id
}
```

## Variables

| Name                  | Description                                    | Type    | Default     |
| --------------------- | ---------------------------------------------- | ------- | ----------- |
| `vpc_cidr_block`      | The CIDR block for the Virtual Private Cloud.  | `string` | `"10.0.0.0/16"` |
| `subnet_cidr_block`   | The CIDR block for the subnet.                 | `string` | `"10.0.1.0/24"` |
| `region`              | The cloud provider region to deploy resources. | `string` | `"us-east-1"` |

## Outputs

| Name      | Description                                    |
| --------- | ---------------------------------------------- |
| `vpc_id`  | The ID of the created VPC.                     |
| `subnet_id` | The ID of the created subnet.                  |
