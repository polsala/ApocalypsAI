variable "bucket_name" {
  description = "The name of the S3 bucket. Must be globally unique."
  type        = string
}

variable "region" {
  description = "The AWS region where the bucket will be created."
  type        = string
}

variable "tags" {
  description = "A map of tags to assign to the bucket."
  type        = map(string)
  default     = {}
}

variable "enable_versioning" {
  description = "Whether to enable versioning for the bucket."
  type        = bool
  default     = true
}

variable "enable_encryption" {
  description = "Whether to enable default server-side encryption (SSE-S3) for the bucket."
  type        = bool
  default     = true
}

variable "lifecycle_rule_days_to_expire" {
  description = "Number of days after which noncurrent object versions will expire."
  type        = number
  default     = 90
}

variable "lifecycle_rule_days_to_transition_to_glacier" {
  description = "Number of days after which noncurrent object versions will transition to GLACIER storage class."
  type        = number
  default     = 30
}
