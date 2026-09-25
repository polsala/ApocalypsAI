variable "bucket_name_prefix" {
  description = "A unique prefix for the S3 bucket name. A random suffix will be added."
  type        = string
  default     = "whispers"
}

variable "enable_s3_versioning" {
  description = "Whether to enable versioning on the S3 bucket."
  type        = bool
  default     = false
}

variable "index_document" {
  description = "The name of the index document (e.g., index.html)."
  type        = string
  default     = "index.html"
}

variable "error_document" {
  description = "The name of the error document (e.g., error.html)."
  type        = string
  default     = "error.html"
}
