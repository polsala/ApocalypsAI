variable "bucket_name" {
  description = "The name of the S3 bucket to create. Must be globally unique."
  type        = string
}

variable "environment" {
  description = "The environment tag for the bucket (e.g., dev, prod, staging)."
  type        = string
  default     = "prod"
}

variable "retention_days_standard" {
  description = "Number of days after which objects in the STANDARD storage class are transitioned to GLACIER."
  type        = number
  default     = 30
}

variable "retention_days_glacier" {
  description = "Number of days after which objects in the GLACIER storage class are expired."
  type        = number
  default     = 365
}
