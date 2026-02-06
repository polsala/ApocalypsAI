variable "bucket_name" {
  description = "The name of the S3 bucket for the chronicle archive."
  type        = string
}

variable "environment" {
  description = "The environment tag for the bucket."
  type        = string
  default     = "production"
}

variable "enable_lifecycle_rules" {
  description = "Whether to enable lifecycle rules for archiving old versions."
  type        = bool
  default     = true
}

variable "noncurrent_version_transition_days" {
  description = "Number of days after which noncurrent versions transition to GLACIER."
  type        = number
  default     = 90
}

variable "noncurrent_version_expiration_days" {
  description = "Number of days after which noncurrent versions expire."
  type        = number
  default     = 365
}
