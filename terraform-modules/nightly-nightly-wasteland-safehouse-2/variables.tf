variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "domain_name" {
  description = "Custom domain for CloudFront (optional)"
  type        = string
  default     = ""
}

variable "index_document" {
  description = "Index document name"
  type        = string
  default     = "index.html"
}

variable "error_document" {
  description = "Error document name"
  type        = string
  default     = "404.html"
}
