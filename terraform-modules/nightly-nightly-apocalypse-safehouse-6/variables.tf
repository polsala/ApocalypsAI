variable "bucket_name" {
  description = "Name of the S3 bucket (must be globally unique)."
  type        = string
}

variable "expiration_days" {
  description = "Number of days after which objects are expired."
  type        = number
  default     = 365
}

variable "enable_logging" {
  description = "Whether to enable S3 server‑side access logging."
  type        = bool
  default     = false
}
