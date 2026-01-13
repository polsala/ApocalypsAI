variable "bucket_name" {
  description = "Name of the S3 bucket."
  type        = string
}

variable "aws_region" {
  description = "AWS region."
  type        = string
  default     = "us-east-1"
}

variable "aws_access_key" {
  description = "AWS access key (dummy for testing)."
  type        = string
  default     = "FAKEACCESSKEY"
}

variable "aws_secret_key" {
  description = "AWS secret key (dummy for testing)."
  type        = string
  default     = "FAKESECRETKEY"
}

variable "environment" {
  description = "Environment tag."
  type        = string
  default     = "dev"
}
