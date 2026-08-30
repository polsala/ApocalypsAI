variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "enable_encryption" {
  description = "Enable server‑side encryption (SSE‑S3)"
  type        = bool
  default     = false
}

variable "transition_days" {
  description = "Days after which objects transition to Glacier"
  type        = number
  default     = 30
}

variable "expiration_days" {
  description = "Days after which objects are permanently deleted"
  type        = number
  default     = 365
}
