variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. The module will append a unique suffix."
  type        = string
  default     = "apocalypsai-chronal-archive"
}

variable "environment" {
  description = "The environment tag for the bucket (e.g., dev, prod, test-timeline)."
  type        = string
  default     = "dev"
}

variable "versioning_enabled" {
  description = "Whether to enable object versioning for the bucket."
  type        = bool
  default     = true
}

variable "tags" {
  description = "A map of tags to assign to the bucket."
  type        = map(string)
  default     = {}
}
