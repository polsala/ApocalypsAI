variable "prefix" {
  description = "A unique prefix for the S3 bucket name. Must be lowercase and globally unique."
  type        = string
}

variable "retention_days" {
  description = "Number of days after which temporal echoes (objects) will be automatically purged from the chamber."
  type        = number
  default     = 7
}

variable "aws_region" {
  description = "The AWS region to deploy the echo chamber."
  type        = string
  default     = "us-east-1" # A common default for AWS resources
}
