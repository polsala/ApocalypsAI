variable "bucket_name_prefix" {
  description = "A unique prefix for the S3 bucket name. Terraform will append a random string."
  type        = string
}

variable "tags" {
  description = "A map of tags to assign to the S3 bucket."
  type        = map(string)
  default     = {}
}

variable "enable_glacier_archive" {
  description = "Set to true to enable a lifecycle rule to archive old data to Glacier."
  type        = bool
  default     = false
}

variable "glacier_archive_days" {
  description = "Number of days after which to transition objects to GLACIER storage class."
  type        = number
  default     = 90
  validation {
    condition     = var.glacier_archive_days > 0
    error_message = "glacier_archive_days must be greater than 0."
  }
}

variable "glacier_expiration_days" {
  description = "Number of days after which to permanently delete objects from GLACIER."
  type        = number
  default     = 3650 # 10 years
  validation {
    condition     = var.glacier_expiration_days > var.glacier_archive_days
    error_message = "glacier_expiration_days must be greater than glacier_archive_days."
  }
}
