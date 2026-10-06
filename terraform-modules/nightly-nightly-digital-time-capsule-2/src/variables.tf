variable "bucket_name_prefix" {
  description = "A unique prefix for the S3 bucket name. The module will append a random string."
  type        = string
}

variable "tags" {
  description = "A map of tags to apply to the S3 bucket."
  type        = map(string)
  default     = {}
}

variable "enable_lifecycle_rules" {
  description = "Whether to enable lifecycle rules for the bucket."
  type        = bool
  default     = false
}

variable "lifecycle_rule_days_to_glacier" {
  description = "Number of days after which non-current versions transition to GLACIER_IR."
  type        = number
  default     = 365
}

variable "lifecycle_rule_days_to_delete" {
  description = "Number of days after which non-current versions and expired object delete markers are permanently deleted."
  type        = number
  default     = 730
}
