variable "bucket_name" {
  description = "Name of the S3 bucket."
  type        = string
}

variable "region" {
  description = "AWS region."
  type        = string
  default     = "us-east-1"
}

variable "expiration_days" {
  description = "Number of days after which objects expire."
  type        = number
  default     = 365
}
