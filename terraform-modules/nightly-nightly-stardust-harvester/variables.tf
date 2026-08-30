variable "bucket_prefix" {
  description = "A unique prefix for the S3 bucket name."
  type        = string
}

variable "environment" {
  description = "The environment tag for resources."
  type        = string
  default     = "dev"
}

variable "enable_versioning" {
  description = "Enable versioning for the S3 bucket."
  type        = bool
  default     = true
}

variable "transition_to_ia_days" {
  description = "Number of days after which to transition objects to STANDARD_IA storage class."
  type        = number
  default     = 30
}

variable "expire_objects_days" {
  description = "Number of days after which to expire objects."
  type        = number
  default     = 90
}

variable "abort_incomplete_multipart_upload_days" {
  description = "Number of days after which to abort incomplete multipart uploads."
  type        = number
  default     = 7
}

variable "enable_notifications" {
  description = "Enable SNS notifications for object events."
  type        = bool
  default     = false
}

variable "notification_filter_prefix" {
  description = "Prefix to filter S3 object notifications (e.g., 'logs/')."
  type        = string
  default     = ""
}
