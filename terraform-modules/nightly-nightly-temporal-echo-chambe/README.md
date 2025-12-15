# Nightly Temporal Echo Chamber (Terraform Module)

This Terraform module provisions an ephemeral AWS EC2 instance, designed to exist for a specified duration before automatically self-terminating. It's perfect for temporary testing environments, quick demos, or isolated experiments where you want to ensure resources are cleaned up without manual intervention.

## Features

*   **Ephemeral EC2 Instance**: Launches a standard EC2 instance.
*   **Self-Destructing**: Automatically schedules its own termination using AWS CloudWatch Events and a Lambda function after a configurable duration.
*   **Temporal Echo**: The termination event can be logged, serving as a 'temporal echo' of its brief existence.
*   **Clean-up**: Ensures no lingering resources, reducing cloud costs and clutter.

## Usage

To use this module, include it in your Terraform configuration and provide the necessary variables.

```terraform
module "my_echo_chamber" {
  source = "./path/to/nightly-temporal-echo-chamber-tf/src"

  aws_region       = "us-east-1" # Or your desired region
  ami_id           = "ami-0abcdef1234567890" # Replace with a valid AMI ID for your region
  instance_type    = "t2.micro"
  duration_minutes = 30 # Instance will terminate after 30 minutes
  tags = {
    Project     = "ApocalypsAI"
    Environment = "EphemeralTest"
  }
}

output "echo_chamber_instance_id" {
  value = module.my_echo_chamber.instance_id
}

output "echo_chamber_public_ip" {
  value = module.my_echo_chamber.public_ip
}
```

## Inputs

| Name             | Description                                                              | Type        | Default    | Required |
| :--------------- | :----------------------------------------------------------------------- | :---------- | :--------- | :------- |
| `aws_region`     | The AWS region to deploy resources into.                                 | `string`    | `us-east-1`| no       |
| `ami_id`         | The AMI ID for the EC2 instance.                                         | `string`    | n/a        | yes      |
| `instance_type`  | The EC2 instance type.                                                   | `string`    | `t2.micro` | no       |
| `duration_minutes`| The duration in minutes after which the instance will self-terminate.    | `number`    | `60`       | no       |
| `tags`           | A map of tags to apply to all resources created by the module.           | `map(string)`| `{}`       | no       |

## Outputs

| Name                        | Description                                          |
| :-------------------------- | :--------------------------------------------------- |
| `instance_id`               | The ID of the created EC2 instance.                  |
| `public_ip`                 | The public IP address of the EC2 instance.           |
| `termination_schedule_name` | The name of the CloudWatch Event Rule for termination.|

## How it Works

1.  **EC2 Instance**: An `aws_instance` is created with the specified AMI and instance type.
2.  **IAM Role & Policy**: An IAM role and policy are created for a Lambda function, granting it permissions to terminate EC2 instances.
3.  **Lambda Function**: A Python Lambda function is deployed. Its sole purpose is to receive an instance ID and region, then call the EC2 `terminate_instances` API.
4.  **CloudWatch Event Rule**: A CloudWatch Event Rule is set up with a `cron` expression derived from `duration_minutes`. This rule triggers the Lambda function after the specified time, passing the EC2 instance's ID and region as environment variables.
5.  **Lambda Permission**: A permission is added to the Lambda function, allowing CloudWatch Events to invoke it.

This setup ensures that the EC2 instance has a finite lifespan and is automatically removed from your AWS account, leaving behind only the logs of its creation and termination as its 'temporal echo'.

## Requirements

*   Terraform CLI (v1.0.0+)
*   AWS CLI configured with appropriate credentials and permissions to create EC2 instances, IAM roles/policies, Lambda functions, and CloudWatch Event Rules.
