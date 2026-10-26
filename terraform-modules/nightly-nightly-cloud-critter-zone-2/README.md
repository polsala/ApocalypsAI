# Nightly Cloud Critter Comfort Zone

## Overview

The `nightly-cloud-critter-zone` is a whimsical Terraform module designed to provision a cozy, minimal cloud habitat for your imaginary digital critter. It sets up essential services that mimic a comfortable living space, ensuring your critter feels right at home in the vast expanse of the cloud.

## Features

*   **Critter Food Bowl (S3 Bucket):** A secure S3 bucket where your critter can store its precious data snacks, logs, or any digital trinkets it collects.
*   **Critter Water Dish (SNS Topic):** An SNS topic to send important notifications, ensuring your critter stays hydrated with timely updates and alerts.
*   **Critter Bedtime Scheduler (CloudWatch Event & Lambda):** A daily scheduled event that triggers a Lambda function to 'tuck in' your critter, ensuring it gets its much-needed digital rest.

## Usage

To deploy your Cloud Critter Comfort Zone, follow these steps:

1.  **Prerequisites:**
    *   [Terraform](https://www.terraform.io/downloads.html) installed.
    *   AWS CLI configured with appropriate credentials and permissions to create S3 buckets, SNS topics, IAM roles, Lambda functions, and CloudWatch events.

2.  **Create a `main.tf` file:**

    Create a new directory for your deployment and add a `main.tf` file:

    ```terraform
    provider "aws" {
      region = "us-east-1" # Or your desired AWS region
    }

    module "my_critter_zone" {
      source = "./src" # Points to the module's source directory

      project_name = "apocalypsai-critters"
      environment  = "prod"
      critter_name = "Fluffy"
      aws_region   = "us-east-1"
    }

    output "food_bowl_name" {
      value       = module.my_critter_zone.food_bowl_name
      description = "The name of the S3 bucket (Critter Food Bowl)"
    }

    output "water_dish_arn" {
      value       = module.my_critter_zone.water_dish_arn
      description = "The ARN of the SNS topic (Critter Water Dish)"
    }

    output "lullaby_lambda_name" {
      value       = module.my_critter_zone.lullaby_lambda_name
      description = "The name of the Lambda function (Critter Lullaby)"
    }
    ```

3.  **Initialize Terraform:**

    ```bash
    terraform init
    ```

4.  **Plan the deployment:**

    Review the resources Terraform will create:

    ```bash
    terraform plan
    ```

5.  **Apply the deployment:**

    Provision the resources in your AWS account:

    ```bash
    terraform apply
    ```

    Type `yes` when prompted.

6.  **Destroy the Comfort Zone (Optional):**

    When your critter decides to migrate, you can tear down its habitat:

    ```bash
    terraform destroy
    ```

    Type `yes` when prompted.

## Module Inputs

| Name         | Description                                  | Type     | Default       | Required |
| :----------- | :------------------------------------------- | :------- | :------------ | :------- |
| `project_name` | The name of the project. Used for resource naming. | `string` | `apocalypsai` | no       |
| `environment`  | The deployment environment. Used for resource naming. | `string` | `dev`         | no       |
| `critter_name` | The name of your cloud critter. Used for resource naming. | `string` | `Whiskers`    | no       |
| `aws_region`   | The AWS region to deploy resources into.     | `string` | `us-east-1`   | no       |

## Module Outputs

| Name                | Description                                  |
| :------------------ | :------------------------------------------- |
| `food_bowl_name`    | The name of the S3 bucket (Critter Food Bowl). |
| `water_dish_arn`    | The ARN of the SNS topic (Critter Water Dish). |
| `lullaby_lambda_name` | The name of the Lambda function (Critter Lullaby). |

## Critter Lore

In the post-apocalyptic digital wasteland, even the smallest data packets yearn for a home. The Cloud Critter Comfort Zone provides a sanctuary, a place where binary beings can frolic, store their bits, and dream of electric sheep. Ensure your critter is well-fed with data and hydrated with notifications, and it will surely bring joy (and perhaps even optimize your cloud spend by being so content!).
