variable "bucket_name" {
  type        = string
  description = "Name of the S3 bucket."
}

variable "index_document" {
  type        = string
  description = "Index document for website."
  default     = "index.html"
}

variable "error_document" {
  type        = string
  description = "Error document for website."
  default     = "error.html"
}

variable "acl" {
  type        = string
  description = "Canned ACL for bucket."
  default     = "public-read"
}
