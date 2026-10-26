variable "bucket_name" {
  description = "The name of the S3 bucket to create."
  type        = string
}

variable "region" {
  description = "The AWS region where the bucket will be created."
  type        = string
  default     = "us-east-1"
}

variable "transition_days_standard_ia" {
  description = "Number of days after which to transition objects to STANDARD_IA storage class."
  type        = number
  default     = 30
}

variable "transition_days_glacier" {
  description = "Number of days after which to transition objects to GLACIER storage class."
  type        = number
  default     = 90
}

variable "expiration_days_noncurrent_versions" {
  description = "Number of days after which to transition noncurrent versions to GLACIER and then expire them."
  type        = number
  default     = 60
}

variable "enable_access_logging" {
  description = "Set to true to enable access logging for the bucket."
  type        = bool
  default     = false
}

variable "log_bucket_name" {
  description = "The name of the S3 bucket where access logs will be stored. Required if enable_access_logging is true."
  type        = string
  default     = null
}

variable "kms_key_id" {
  description = "Optional: The ARN of the KMS key to use for server-side encryption. If null, AES256 will be used."
  type        = string
  default     = null
}
