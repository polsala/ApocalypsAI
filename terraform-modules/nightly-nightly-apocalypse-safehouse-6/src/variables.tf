variable "bucket_name" {
  description = "Custom bucket name (optional)."
  type        = string
  default     = ""
}

variable "aws_region" {
  description = "AWS region to deploy resources."
  type        = string
  default     = "us-east-1"
}
