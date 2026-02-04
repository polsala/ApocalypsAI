# nightly-terraform-wasteland-shelter-deploy

A Terraform module that provisions essential cloud infrastructure for post-apocalyptic survivalist hideouts. Designed for resilience, redundancy, and resource efficiency.

## Features

- Provisions a VPC with isolated subnets
- Deploys a resilient EC2 instance with survival tooling pre-installed
- Sets up an S3 bucket for long-term storage of survival caches
- Enables CloudWatch monitoring for anomaly detection

## Usage

```hcl
module "wasteland_shelter" {
  source = "./terraform-modules/nightly-terraform-wasteland-shelter-deploy"

  region       = "us-west-1"
  shelter_name = "alpha-bunker"
}
```

## Inputs

| Name         | Description                  | Type   | Default |
|--------------|------------------------------|--------|---------|
| region       | AWS region for deployment    | string | n/a     |
| shelter_name | Unique name for the shelter  | string | n/a     |

## Outputs

| Name              | Description                        |
|-------------------|------------------------------------|
| shelter_instance  | Public IP of the shelter instance  |
| survival_bucket   | Name of the survival cache bucket |
