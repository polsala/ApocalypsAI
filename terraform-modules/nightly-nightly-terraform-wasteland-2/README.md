# Terraform Wasteland Outpost Module

This module provisions a post-apocalyptic themed infrastructure on AWS, including a VPC, subnets, security groups, and EC2 instances tagged with survival-themed metadata.

## Features

- Provisions a VPC with public and private subnets
- Launches a configurable number of EC2 instances
- Applies survival-themed tags to all resources
- Outputs instance IPs and VPC ID

## Usage

```hcl
module "wasteland_outpost" {
  source = "./terraform-wasteland-outpost"

  region       = "us-west-2"
  outpost_name = "alpha-site"
  instance_count = 3
}

output "vpc_id" {
  value = module.wasteland_outpost.vpc_id
}

output "public_ips" {
  value = module.wasteland_outpost.public_ips
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| region | AWS region | `string` | n/a | yes |
| outpost_name | Name of the outpost | `string` | n/a | yes |
| instance_count | Number of EC2 instances | `number` | `1` | no |

## Outputs

| Name | Description |
|------|-------------|
| vpc_id | ID of the created VPC |
| public_ips | List of public IPs of instances |
