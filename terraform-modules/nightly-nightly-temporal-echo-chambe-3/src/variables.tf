variable "bucket_name_prefix" {
  description = "A unique prefix for the S3 bucket name. A random suffix will be added."
  type        = string
}

variable "retention_days" {
  description = "Number of days after which objects in the bucket will be automatically expired."
  type        = number
  default     = 7
}

variable "environment" {
  description = "Environment tag for the bucket."
  type        = string
  default     = "development"
}
