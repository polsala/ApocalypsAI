variable "bucket_name_prefix" {
  description = "A unique prefix for the S3 bucket name."
  type        = string
}

variable "initial_message" {
  description = "The initial message to display on the signal fire page."
  type        = string
  default     = "Beacon online. Awaiting instructions."
}

variable "aws_region" {
  description = "The AWS region to deploy resources in."
  type        = string
  default     = "us-east-1"
}

provider "aws" {
  region = var.aws_region
}
