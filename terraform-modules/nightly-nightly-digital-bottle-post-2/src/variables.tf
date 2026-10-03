variable "bucket_name_prefix" {
  description = "Prefix for the S3 bucket name. A unique suffix will be appended."
  type        = string
}

variable "message_retention_days" {
  description = "Number of days after which messages (objects) will be expired."
  type        = number
  default     = 30
  validation {
    condition     = var.message_retention_days > 0
    error_message = "message_retention_days must be greater than 0."
  }
}

variable "enable_public_read" {
  description = "Set to true to allow public read access to objects in the bucket."
  type        = bool
  default     = false
}

variable "tags" {
  description = "A map of tags to assign to the bucket."
  type        = map(string)
  default     = {}
}

variable "versioning_enabled" {
  description = "Whether to enable versioning for the bucket."
  type        = bool
  default     = true
}
