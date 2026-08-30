variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. A unique suffix will be added."
  type        = string
  default     = "chrono-cache"
}

variable "expiration_days" {
  description = "Number of days after which objects in the bucket will expire."
  type        = number
  default     = 30
}

variable "region" {
  description = "The AWS region to create the bucket in."
  type        = string
}

# Configure the AWS provider
provider "aws" {
  region = var.region
}
