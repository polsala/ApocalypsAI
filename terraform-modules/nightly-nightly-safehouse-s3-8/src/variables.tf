variable "bucket_name_prefix" {
  description = "Prefix for the S3 bucket name."
  type        = string
}

variable "tags" {
  description = "Tags to apply to the bucket."
  type        = map(string)
  default     = {}
}

variable "aws_region" {
  description = "AWS region."
  type        = string
  default     = "us-east-1"
}
