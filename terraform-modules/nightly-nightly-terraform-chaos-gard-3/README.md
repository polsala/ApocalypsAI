# Nightly Terraform Chaos Garden

A whimsical Terraform module that creates a garden of resources and then randomly destroys them for chaos engineering.

## Features

- Creates a variety of AWS resources (S3 buckets, DynamoDB tables, Lambda functions)
- Randomly destroys resources based on a configurable chaos factor
- Provides a dashboard for monitoring the garden's health
- Includes automated tests with mock AWS resources

## Usage

```hcl
module "chaos_garden" {
  source = "./modules/chaos_garden"
  
  garden_name = "apocalypsgarden"
  chaos_factor = 0.3  # 30% chance of resource destruction
  
  # Resource configurations
  s3_buckets = ["flowers", "trees", "bushes"]
  dynamodb_tables = ["insects", "birds", "soil"]
  lambda_functions = ["watering", "pruning", "harvesting"]
}
```

## Variables

- `garden_name`: Name prefix for all resources
- `chaos_factor`: Probability (0.0-1.0) of resource destruction
- `s3_buckets`: List of S3 bucket names to create
- `dynamodb_tables`: List of DynamoDB table names to create
- `lambda_functions`: List of Lambda function names to create

## Outputs

- `garden_health`: Current health status of the garden
- `surviving_resources`: List of resources that survived the chaos
- `destroyed_resources`: List of resources that were destroyed
