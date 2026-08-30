variable "bucket_name_prefix" {
  description = "A unique prefix for the S3 bucket name. Terraform will append a unique suffix."
  type        = string
  default     = "apocalypsai-ephemeral-cache-"
}

variable "expiration_days" {
  description = "Number of days after which objects in the bucket will be automatically deleted."
  type        = number
  default     = 7
  validation {
    condition     = var.expiration_days >= 1
    error_message = "Expiration days must be at least 1."
  }
}
