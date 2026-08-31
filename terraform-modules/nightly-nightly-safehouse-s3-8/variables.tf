variable "bucket_name" {
  description = "Name of the S3 bucket (must be globally unique)"
  type        = string
}

variable "versioning_enabled" {
  description = "Enable versioning on the bucket"
  type        = bool
  default     = true
}

variable "lifecycle_days" {
  description = "Number of days after which objects expire"
  type        = number
  default     = 30
}
