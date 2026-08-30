# Nightly Cloud Scavenger Hunt

This Terraform module provisions a collection of AWS cloud resources, each tagged with whimsical "post-apocalyptic" metadata. The purpose is to create a fun, yet practical, "scavenger hunt" scenario for users to practice discovering, identifying, and inventorying cloud resources based on their tags and properties. It's an excellent tool for learning cloud resource management, tagging strategies, and basic Terraform usage.

## Features

*   Provisions various AWS resources: S3 bucket, EC2 instance, Lambda function, DynamoDB table.
*   Applies consistent and whimsical tags (e.g., `loot_level`, `hidden_location`, `survival_kit_id`).
*   Configurable prefix for resource naming to avoid conflicts.
*   Outputs key identifiers for the provisioned resources.

## Usage

1.  **Prerequisites**:
    *   [Terraform](https://www.terraform.io/downloads.html) installed.
    *   AWS credentials configured (e.g., via `~/.aws/credentials` or environment variables).

2.  **Module Integration**:
    Create a `main.tf` file in your Terraform project:

    ```terraform
    module "scavenger_hunt" {
      source = "./path/to/nightly-cloud-scavenger-hunt" # Adjust path if not local
      
      prefix          = "apocalypsai-hunt"
      region          = "us-east-1"
      instance_type   = "t2.micro" # Ensure this is available in your region and within limits
      lambda_runtime  = "nodejs18.x"
    }

    output "s3_bucket_name" {
      value = module.scavenger_hunt.s3_bucket_name
    }

    output "ec2_instance_id" {
      value = module.scavenger_hunt.ec2_instance_id
    }

    output "lambda_function_name" {
      value = module.scavenger_hunt.lambda_function_name
    }

    output "dynamodb_table_name" {
      value = module.scavenger_hunt.dynamodb_table_name
    }
    ```

3.  **Initialize and Apply**:

    ```bash
    terraform init
    terraform plan
    terraform apply
    ```

    Remember to run `terraform destroy` when you're done to avoid incurring unexpected costs.

## Inputs

| Name              | Description                                     | Type     | Default       | Required |
| :---------------- | :---------------------------------------------- | :------- | :------------ | :------- |
| `prefix`          | A prefix for all resource names.                | `string` | `"apocalypsai"` | no       |
| `region`          | AWS region to deploy resources into.            | `string` | `"us-east-1"` | no       |
| `instance_type`   | EC2 instance type.                              | `string` | `"t2.micro"`  | no       |
| `lambda_runtime`  | AWS Lambda runtime.                             | `string` | `"nodejs18.x"`| no       |

## Outputs

| Name                     | Description                                     |
| :----------------------- | :---------------------------------------------- |
| `s3_bucket_name`         | The name of the provisioned S3 bucket.          |
| `ec2_instance_id`        | The ID of the provisioned EC2 instance.         |
| `lambda_function_name`   | The name of the provisioned Lambda function.    |
| `dynamodb_table_name`    | The name of the provisioned DynamoDB table.     |

## Scavenger Hunt Challenge

Once the resources are deployed, try to find them using the AWS Console, AWS CLI, or SDKs. Look for tags like:
*   `Environment = "ApocalypsAI"`
*   `Project = "ScavengerHunt"`
*   `LootLevel = "Rare"`
*   `HiddenLocation = "SectorGamma"`
*   `SurvivalKitID = "Alpha-7"`

Can you list all resources with `LootLevel = "Rare"`? Can you find the `SurvivalKitID` for the EC2 instance?
