variable "bucket_name" {
  description = "Base name for the S3 bucket."
  type        = string
}

variable "tags" {
  description = "Tags to apply to the bucket."
  type        = map(string)
  default     = {}
}

variable "aws_region" {
  description = "AWS region for the bucket."
  type        = string
  default     = "us-east-1"
}
