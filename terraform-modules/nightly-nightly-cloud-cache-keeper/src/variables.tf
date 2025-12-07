variable "bucket_name" {
  description = "The name of the S3 bucket to create."
  type        = string
}

variable "enable_versioning" {
  description = "Whether to enable versioning on the S3 bucket."
  type        = bool
  default     = true
}

variable "transition_to_glacier_days" {
  description = "Number of days after which to transition objects to GLACIER storage class."
  type        = number
  default     = 30
}

variable "expire_after_days" {
  description = "Number of days after which to expire objects (delete them)."
  type        = number
  default     = 365
}

variable "environment" {
  description = "The environment tag for the bucket (e.g., 'dev', 'prod', 'wasteland')."
  type        = string
  default     = "wasteland"
}

variable "tags" {
  description = "A map of additional tags to apply to the bucket."
  type        = map(string)
  default     = {}
}
