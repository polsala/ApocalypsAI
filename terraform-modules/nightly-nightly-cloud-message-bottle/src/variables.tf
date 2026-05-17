variable "bucket_name_prefix" {
  description = "A unique prefix for the S3 bucket name. A random suffix will be appended."
  type        = string
}

variable "expiration_days" {
  description = "Number of days after which objects in the bucket will be automatically deleted."
  type        = number
  default     = 1
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
