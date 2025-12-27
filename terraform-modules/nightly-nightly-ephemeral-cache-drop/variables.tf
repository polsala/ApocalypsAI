variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. A unique suffix will be appended."
  type        = string
  default     = "apocalypsai-cache"
}

variable "expiration_days" {
  description = "Number of days after which objects in the bucket will expire and be deleted."
  type        = number
  default     = 7
  validation {
    condition     = var.expiration_days >= 1
    error_message = "Expiration days must be at least 1."
  }
}

variable "tags" {
  description = "A map of tags to assign to the S3 bucket."
  type        = map(string)
  default     = {}
}
