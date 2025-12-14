variable "bucket_name" {
  description = "The name of the S3 bucket."
  type        = string
}

variable "enable_versioning" {
  description = "Whether to enable versioning."
  type        = bool
  default     = true
}

variable "lifecycle_rules" {
  description = "List of lifecycle rules."
  type = list(object({
    prefix          = string
    enabled         = bool
    expiration_days = number
  }))
  default = []
}
