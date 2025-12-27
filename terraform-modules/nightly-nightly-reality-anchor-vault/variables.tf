variable "bucket_name" {
  description = "The name for the S3 bucket. Must be globally unique."
  type        = string
}

variable "environment" {
  description = "The environment (e.g., dev, staging, production). Used for tagging."
  type        = string
  default     = "dev"
}

variable "retention_days" {
  description = "Number of days objects in the vault should be immutable (Object Lock in COMPLIANCE mode)."
  type        = number
  default     = 365
  validation {
    condition     = var.retention_days >= 1
    error_message = "Retention days must be at least 1."
  }
}

variable "tags" {
  description = "A map of tags to assign to the bucket."
  type        = map(string)
  default     = {}
}
