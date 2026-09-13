variable "bucket_name" {
  description = "The name for the S3 bucket. Must be globally unique."
  type        = string
}

variable "environment" {
  description = "Environment tag for the bucket (e.g., dev, prod)."
  type        = string
  default     = "dev"
}

variable "project" {
  description = "Project tag for the bucket."
  type        = string
  default     = "default"
}

variable "retention_days_to_glacier" {
  description = "Number of days after which noncurrent versions transition to GLACIER."
  type        = number
  default     = 30
}

variable "expiration_days_noncurrent" {
  description = "Number of days after which noncurrent versions are permanently deleted."
  type        = number
  default     = 90
}

variable "enable_access_logging" {
  description = "Whether to enable S3 access logging for the bucket."
  type        = bool
  default     = false
}

variable "logging_bucket_name" {
  description = "The name of the S3 bucket where access logs will be stored. Required if enable_access_logging is true."
  type        = string
  default     = null
}
