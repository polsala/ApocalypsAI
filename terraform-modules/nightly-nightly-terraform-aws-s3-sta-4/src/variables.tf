variable "bucket_name" {
  description = "Name of the S3 bucket (must be globally unique)."
  type        = string
}

variable "enable_cdn" {
  description = "Whether to create a CloudFront distribution."
  type        = bool
  default     = false
}

variable "index_document" {
  description = "S3 website index document."
  type        = string
  default     = "index.html"
}

variable "error_document" {
  description = "S3 website error document."
  type        = string
  default     = "error.html"
}
