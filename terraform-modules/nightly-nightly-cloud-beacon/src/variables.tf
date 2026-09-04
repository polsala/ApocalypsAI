variable "bucket_name_prefix" {
  description = "A unique prefix for the S3 bucket name."
  type        = string
}

variable "index_document" {
  description = "The default document for the website."
  type        = string
  default     = "index.html"
}

variable "error_document" {
  description = "The error document for the website."
  type        = string
  default     = "error.html"
}

variable "tags" {
  description = "A map of tags to apply to the created resources."
  type        = map(string)
  default     = {}
}
