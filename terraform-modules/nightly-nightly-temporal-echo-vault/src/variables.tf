variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. A unique suffix will be added."
  type        = string
}

variable "region" {
  description = "The AWS region where the S3 bucket will be created."
  type        = string
}

variable "echo_chamber_retention_days" {
  description = "Number of days before current object versions transition to Intelligent-Tiering."
  type        = number
  default     = 30
}

variable "echo_chamber_glacier_days" {
  description = "Number of days before non-current object versions transition to Glacier."
  type        = number
  default     = 90
}

variable "echo_chamber_decay_days" {
  description = "Number of days before non-current object versions are permanently deleted."
  type        = number
  default     = 365
}

variable "enable_versioning" {
  description = "Whether to enable versioning on the S3 bucket."
  type        = bool
  default     = true
}
