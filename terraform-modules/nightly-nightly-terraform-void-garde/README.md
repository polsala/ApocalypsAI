# Nightly Terraform Void Garden

A whimsical, self-contained Terraform module that creates a cloud garden in AWS. This module provisions:
- A VPC with subnets
- An auto-scaling group of t2.micro instances running a simple garden web server
- Security groups with whimsical naming
- Resource limits and alerts
- A hidden easter egg accessible via a specific path

## Usage

```hcl
module "void_garden" {
  source = "./modules/nightly-terraform-void-garden"

  garden_name = "my-void-garden"
  environment = "dev"
  max_instances = 3
  min_instances = 1
  desired_capacity = 2
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| garden_name | Name of the garden | string | "void-garden" | no |
| environment | Environment tag | string | "dev" | no |
| max_instances | Maximum number of instances | number | 3 | no |
| min_instances | Minimum number of instances | number | 1 | no |
| desired_capacity | Desired number of instances | number | 2 | no |

## Outputs

| Name | Description |
|------|-------------|
| garden_url | URL of the garden load balancer |
| easter_egg_path | Path to the hidden easter egg |
