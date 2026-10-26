variable "bucket_name" {
  description = "The name of the S3 bucket for the time capsule."
  type        = string
}

variable "object_lock_mode" {
  description = "The object lock retention mode. Can be 'GOVERNANCE' or 'COMPLIANCE'."
  type        = string
  default     = "GOVERNANCE"
  validation {
    condition     = contains(["GOVERNANCE", "COMPLIANCE"], var.object_lock_mode)
    error_message = "Object lock mode must be 'GOVERNANCE' or 'COMPLIANCE'."
  }
}

variable "object_lock_days" {
  description = "The number of days for object lock retention."
  type        = number
  default     = 3650 # 10 years
  validation {
    condition     = var.object_lock_days > 0
    error_message = "Object lock days must be a positive number."
  }
}

variable "archive_transition_days" {
  description = "The number of days after which objects transition to GLACIER_DEEP_ARCHIVE."
  type        = number
  default     = 90 # Transition after 3 months
  validation {
    condition     = var.archive_transition_days > 0
    error_message = "Archive transition days must be a positive number."
  }
}

variable "tags" {
  description = "A map of tags to assign to the bucket."
  type        = map(string)
  default     = {}
}
