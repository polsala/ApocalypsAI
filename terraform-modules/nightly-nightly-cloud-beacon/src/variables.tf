variable "bucket_name" {
  description = "The name of the S3 bucket for the static website beacon. Must be globally unique."
  type        = string
}

variable "aws_region" {
  description = "The AWS region where the S3 bucket will be created."
  type        = string
  default     = "us-east-1"
}

variable "tags" {
  description = "A map of tags to assign to the S3 bucket."
  type        = map(string)
  default     = {}
}
