variable "bucket_name" {
  description = "The name of the S3 bucket to create for the archive vault. Must be globally unique."
  type        = string
}

variable "region" {
  description = "The AWS region where the S3 bucket will be created."
  type        = string
  default     = "us-east-1"
}

variable "enable_versioning" {
  description = "Whether to enable versioning for the S3 bucket."
  type        = bool
  default     = true
}

variable "enable_object_lock" {
  description = "Whether to enable S3 Object Lock for immutability. This must be set at bucket creation."
  type        = bool
  default     = false
}

variable "retention_mode" {
  description = "The S3 Object Lock retention mode (GOVERNANCE or COMPLIANCE). Required if enable_object_lock is true."
  type        = string
  default     = "GOVERNANCE"
  validation {
    condition     = !var.enable_object_lock || contains(["GOVERNANCE", "COMPLIANCE"], var.retention_mode)
    error_message = "Retention mode must be 'GOVERNANCE' or 'COMPLIANCE' when enable_object_lock is true."
  }
}

variable "retention_period_days" {
  description = "The number of days for S3 Object Lock retention. Required if enable_object_lock is true."
  type        = number
  default     = 30
  validation {
    condition     = !var.enable_object_lock || var.retention_period_days > 0
    error_message = "Retention period must be a positive number of days when enable_object_lock is true."
  }
}
