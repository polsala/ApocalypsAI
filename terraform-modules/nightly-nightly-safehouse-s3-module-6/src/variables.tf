variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "force_destroy" {
  description = "Allow destroying a non‑empty bucket"
  type        = bool
  default     = false
}

variable "block_public_access" {
  description = "Enable S3 Block Public Access"
  type        = bool
  default     = true
}
