variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. A unique suffix will be appended."
  type        = string
}

variable "retention_years" {
  description = "The number of years for object lock retention and lifecycle expiration."
  type        = number
  default     = 100
  validation {
    condition     = var.retention_years >= 1
    error_message = "Retention years must be at least 1."
  }
}

variable "tags" {
  description = "A map of tags to assign to the bucket."
  type        = map(string)
  default     = {}
}
