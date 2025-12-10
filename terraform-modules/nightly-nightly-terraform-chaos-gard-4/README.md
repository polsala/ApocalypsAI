# Nightly Terraform Chaos Garden

A whimsical Terraform module that creates a garden of chaos resources for testing infrastructure resilience. Perfect for chaos engineering experiments and testing your disaster recovery procedures!

## Features

- Creates a variety of AWS resources (S3 buckets, EC2 instances, Lambda functions)
- Randomizes resource names and configurations for each apply
- Includes chaos scenarios like random instance termination and bucket deletion
- Provides a dashboard for monitoring your chaos garden

## Usage

```hcl
module "chaos_garden" {
  source = "./modules/chaos_garden"

  garden_name = "my-chaos-garden"
  region      = "us-west-2"
  chaos_level = 3  # 1-5, higher means more chaos
}
```

## Variables

| Variable      | Description                              | Type   | Default |
|---------------|------------------------------------------|--------|---------|
| garden_name   | Name for your chaos garden               | string | "chaos" |
| region        | AWS region to deploy resources           | string | "us-west-2" |
| chaos_level   | Level of chaos (1-5)                     | number | 3       |
| enable_chaos  | Enable chaos scenarios                   | bool   | true    |

## Outputs

| Output           | Description                              |
|------------------|------------------------------------------|
| garden_url       | URL to the chaos garden dashboard        |
| chaos_resources  | List of created chaos resources          |
| chaos_schedule   | Cron schedule for chaos events           |

## License

MIT License - Use at your own risk!

> **Warning**: This module is designed to create chaos. Do not use in production environments.
