variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. A unique suffix will be appended."
  type        = string
}

variable "retention_days" {
  description = "The number of days after which objects in the bucket will expire."
  type        = number
  default     = 30
  validation {
    condition     = var.retention_days > 0
    error_message = "Retention days must be a positive number."
  }
}

variable "tags" {
  description = "A map of tags to assign to the S3 bucket."
  type        = map(string)
  default     = {}
}
