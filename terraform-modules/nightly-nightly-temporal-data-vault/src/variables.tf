variable "bucket_name" {
  description = "The name of the S3 bucket to create."
  type        = string
}

variable "enable_versioning" {
  description = "Whether to enable versioning for the S3 bucket."
  type        = bool
  default     = true
}

variable "enable_lifecycle_rules" {
  description = "Whether to enable lifecycle rules for the S3 bucket."
  type        = bool
  default     = true
}

variable "noncurrent_version_expiration_days" {
  description = "Number of days after which noncurrent versions of objects will be permanently deleted."
  type        = number
  default     = 90
}

variable "transition_current_to_ia_days" {
  description = "Number of days after which current versions of objects will be transitioned to STANDARD_IA storage class. Set to 0 to disable."
  type        = number
  default     = 30
}

variable "transition_noncurrent_to_ia_days" {
  description = "Number of days after which noncurrent versions of objects will be transitioned to STANDARD_IA storage class. Set to 0 to disable."
  type        = number
  default     = 60
}

variable "tags" {
  description = "A map of tags to assign to the bucket."
  type        = map(string)
  default     = {}
}
