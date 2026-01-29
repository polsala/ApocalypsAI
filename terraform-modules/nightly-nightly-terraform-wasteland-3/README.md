# nightly-terraform-wasteland-shelter

A Terraform module to provision a post-apocalyptic survival shelter with essential infrastructure: solar power, water filtration, and secure networking.

## Features

- Provisions a virtual private cloud (VPC) for secure networking
- Deploys a solar-powered virtual machine for energy-efficient compute
- Sets up a water filtration simulation using a managed database
- Includes security groups and IAM roles for access control

## Usage

```hcl
module "wasteland_shelter" {
  source = "./terraform-modules/nightly-terraform-wasteland-shelter"

  region           = "us-west-1"
  shelter_name     = "survivor-base-01"
  instance_type    = "t3.micro"
  db_instance_class = "db.t3.micro"
}
```

## Inputs

| Name              | Description                     | Type   | Default      |
|-------------------|----------------------------------|--------|--------------|
| region            | AWS region                      | string | `us-west-1`  |
| shelter_name      | Name of the shelter             | string | `shelter`    |
| instance_type     | Compute instance type           | string | `t3.micro`   |
| db_instance_class | Database instance class         | string | `db.t3.micro`|

## Outputs

| Name              | Description                     |
|-------------------|----------------------------------|
| shelter_ip        | Public IP of the shelter VM     |
| db_endpoint       | Database endpoint               |
| vpc_id            | ID of the created VPC           |
