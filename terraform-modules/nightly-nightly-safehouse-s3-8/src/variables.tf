variable "bucket_name" {
  description = "Name of the S3 bucket for the safehouse."
  type        = string
}

variable "aws_region" {
  description = "AWS region to create the bucket in."
  type        = string
  default     = "us-east-1"
}
