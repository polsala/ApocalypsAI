variable "bucket_name" {
  description = "Name of the S3 bucket."
  type        = string
}

variable "enable_secret" {
  description = "Create a Secrets Manager secret with a random password."
  type        = bool
  default     = false
}

variable "aws_region" {
  description = "AWS region for the resources."
  type        = string
  default     = "us-east-1"
}
