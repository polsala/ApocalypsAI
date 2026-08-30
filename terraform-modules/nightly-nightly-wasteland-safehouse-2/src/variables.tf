variable "bucket_name" {
  description = "Name of the S3 bucket."
  type        = string
}

variable "radiation_level" {
  description = "Radiation level tag for the bucket."
  type        = string
  default     = "low"
  validation {
    condition     = contains(["low", "moderate", "high"], var.radiation_level)
    error_message = "radiation_level must be one of low, moderate, high."
  }
}

variable "aws_region" {
  description = "AWS region."
  type        = string
  default     = "us-east-1"
}
