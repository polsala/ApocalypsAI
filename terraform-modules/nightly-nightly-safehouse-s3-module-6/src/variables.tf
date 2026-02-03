variable "bucket_name" {
  description = "Name of the S3 bucket (must be globally unique)"
  type        = string
}

variable "retention_days" {
  description = "Number of days to retain objects before automatic deletion"
  type        = number
  default     = 365
}

variable "password_length" {
  description = "Length of the generated random password"
  type        = number
  default     = 32
}

variable "password_special" {
  description = "Whether to include special characters in the password"
  type        = bool
  default     = true
}

variable "aws_region" {
  description = "AWS region for the bucket"
  type        = string
  default     = "us-east-1"
}
