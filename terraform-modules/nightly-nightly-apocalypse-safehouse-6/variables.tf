variable "bucket_name" {
  description = "Name of the S3 bucket (must be globally unique)."
  type        = string
}

variable "region" {
  description = "AWS region where the bucket will be created."
  type        = string
  default     = "us-east-1"
}

variable "initial_supply" {
  description = "Optional text for a starter object (welcome.txt)."
  type        = string
  default     = ""
}
