variable "bucket_name" {
  description = "The name of the S3 bucket to create. Must be globally unique."
  type        = string
}

variable "region" {
  description = "The AWS region where the S3 bucket will be created."
  type        = string
  default     = "us-east-1"
}

variable "tags" {
  description = "A map of tags to assign to the bucket."
  type        = map(string)
  default     = {}
}

variable "glacier_ir_transition_days" {
  description = "Number of days after object creation to transition to GLACIER_IR storage class."
  type        = number
  default     = 30
}

variable "deep_archive_transition_days" {
  description = "Number of days after object creation to transition to DEEP_ARCHIVE storage class."
  type        = number
  default     = 90
}

variable "expiration_days" {
  description = "Number of days after object creation to expire (delete) the object. Set to null for no expiration."
  type        = number
  default     = null
}
