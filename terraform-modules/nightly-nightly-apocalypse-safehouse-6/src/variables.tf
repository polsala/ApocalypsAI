variable "bucket_name" {
  description = "Name of the S3 bucket (must be globally unique)."
  type        = string
}

variable "region" {
  description = "AWS region where the bucket will be created."
  type        = string
  default     = "us-east-1"
}
