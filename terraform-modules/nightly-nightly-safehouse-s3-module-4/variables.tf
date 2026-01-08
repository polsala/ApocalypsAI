variable "bucket_name" {
  description = "Name of the mock S3 bucket"
  type        = string
  default     = "apocalypse-safehouse"
}

variable "versioning" {
  description = "Whether versioning is enabled (informational only)"
  type        = bool
  default     = true
}
