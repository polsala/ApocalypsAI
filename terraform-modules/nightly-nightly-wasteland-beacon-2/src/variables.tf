variable "beacon_name" {
  description = "A unique name for the beacon resources."
  type        = string
}

variable "schedule_expression" {
  description = "The schedule expression for the beacon (e.g., rate(1 hour) or cron(0 0 * * ? *))."
  type        = string
}

variable "aws_region" {
  description = "The AWS region to deploy the beacon in."
  type        = string
}

# Configure the AWS provider
provider "aws" {
  region = var.aws_region
}
