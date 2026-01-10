variable "bucket_name_prefix" {
  description = "Prefix for the S3 bucket name. A random suffix will be appended."
  type        = string
}

variable "region" {
  description = "AWS region to deploy the S3 bucket."
  type        = string
}

variable "decay_period_days" {
  description = "Number of days after which the bucket and its contents will be automatically deleted."
  type        = number
  default     = 7
  validation {
    condition     = var.decay_period_days > 0
    error_message = "The decay_period_days must be a positive number."
  }
}
