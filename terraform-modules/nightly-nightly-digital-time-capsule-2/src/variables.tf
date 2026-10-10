variable "bucket_name_prefix" {
  description = "Prefix for the S3 bucket name. A random suffix will be appended."
  type        = string
  default     = "apocalypsai-time-capsule-"
}

variable "region" {
  description = "AWS region where the S3 bucket will be created."
  type        = string
  default     = "us-east-1"
}

variable "enable_versioning" {
  description = "Whether to enable versioning for the S3 bucket."
  type        = bool
  default     = true
}

variable "glacier_transition_days" {
  description = "Number of days after which objects (and non-current versions) will transition to GLACIER storage class."
  type        = number
  default     = 365 # 1 year
}

variable "expiration_days" {
  description = "Number of days after which objects (and non-current versions) will expire and be permanently deleted."
  type        = number
  default     = 1825 # 5 years
}
