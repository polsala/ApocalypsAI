variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. A unique suffix will be appended."
  type        = string
  default     = "chrono-cache"
}

variable "expiration_days" {
  description = "Number of days after which objects in the bucket will be expired/deleted."
  type        = number
  default     = 7
  validation {
    condition     = var.expiration_days > 0
    error_message = "Expiration days must be a positive number."
  }
}

variable "aws_region" {
  description = "The AWS region where the S3 bucket will be created."
  type        = string
  default     = "us-east-1"
}
