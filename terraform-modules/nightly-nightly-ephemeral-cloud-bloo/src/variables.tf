variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name to ensure uniqueness."
  type        = string
  default     = "apocalypsai"
}

variable "expiration_days" {
  description = "Number of days after which objects in the bucket will be automatically deleted (wilting period)."
  type        = number
  default     = 30
  validation {
    condition     = var.expiration_days > 0
    error_message = "Expiration days must be a positive number."
  }
}

variable "enable_public_access" {
  description = "Set to true to enable public access for static website hosting. WARNING: This makes your bucket content publicly readable."
  type        = bool
  default     = false
}

variable "tags" {
  description = "A map of tags to assign to the S3 bucket."
  type        = map(string)
  default     = {}
}
