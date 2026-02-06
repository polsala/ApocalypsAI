variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. A unique suffix will be appended."
  type        = string
}

variable "environment" {
  description = "The environment tag for the bucket (e.g., dev, prod)."
  type        = string
  default     = "dev"
}

variable "retention_days" {
  description = "Number of days after which objects in the bucket will be permanently deleted."
  type        = number
  default     = 30
}

variable "transition_days_to_ia" {
  description = "Number of days after which objects will transition to S3 Glacier Instant Retrieval."
  type        = number
  default     = 7
}
