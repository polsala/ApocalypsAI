variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. A unique suffix will be appended."
  type        = string
}

variable "region" {
  description = "The AWS region where the S3 bucket will be created."
  type        = string
}

variable "enable_replication" {
  description = "Whether to enable cross-region replication."
  type        = bool
  default     = false
}

variable "replication_destination_bucket_arn" {
  description = "ARN of the destination bucket for replication. Required if enable_replication is true."
  type        = string
  default     = null
}

variable "enable_glacier_archive" {
  description = "Whether to enable lifecycle rules to transition objects to Glacier."
  type        = bool
  default     = false
}

variable "glacier_transition_days" {
  description = "Number of days after which to transition objects to Glacier."
  type        = number
  default     = 30
}
