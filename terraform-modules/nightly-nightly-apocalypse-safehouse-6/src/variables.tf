variable "bucket_prefix" {
  description = "Prefix for the bucket name"
  type        = string
  default     = "safehouse"
}

variable "aws_region" {
  description = "AWS region for the bucket"
  type        = string
  default     = "us-east-1"
}
