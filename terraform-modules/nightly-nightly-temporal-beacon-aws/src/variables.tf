variable "bucket_name_prefix" {
  description = "Prefix for the S3 bucket name. A unique suffix will be appended."
  type        = string
}

variable "environment" {
  description = "The environment tag for the S3 bucket."
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "The AWS region to deploy the S3 bucket in."
  type        = string
  default     = "us-east-1"
}
