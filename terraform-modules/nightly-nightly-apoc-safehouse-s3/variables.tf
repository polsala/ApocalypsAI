variable "bucket_name_prefix" {
  description = "Prefix for the bucket name (lowercase, alphanumeric, hyphens)"
  type        = string
}

variable "versioning_enabled" {
  description = "Enable S3 versioning"
  type        = bool
  default     = true
}

variable "lifecycle_days" {
  description = "Days after which non‑current versions are deleted"
  type        = number
  default     = 30
}
