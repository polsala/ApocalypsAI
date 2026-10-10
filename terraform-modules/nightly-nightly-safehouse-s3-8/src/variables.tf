variable "bucket_name" {
  description = "Name of the S3 bucket."
  type        = string
}

variable "aws_region" {
  description = "AWS region for the bucket."
  type        = string
  default     = "us-east-1"
}
