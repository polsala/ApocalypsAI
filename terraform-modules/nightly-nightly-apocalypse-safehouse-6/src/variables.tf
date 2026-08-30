variable "bucket_name" {
  description = "Base name for the S3 bucket."
  type        = string
}

variable "enable_random_suffix" {
  description = "Whether to append a random suffix to avoid name collisions."
  type        = bool
  default     = true
}

variable "aws_region" {
  description = "AWS region."
  type        = string
  default     = "us-east-1"
}
