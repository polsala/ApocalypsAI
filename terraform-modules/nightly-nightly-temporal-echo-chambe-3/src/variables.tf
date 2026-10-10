variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. A unique suffix will be appended."
  type        = string
}

variable "content_html" {
  description = "The initial HTML content for the index.html file in the S3 bucket."
  type        = string
}

variable "tags" {
  description = "A map of tags to apply to all resources created by the module."
  type        = map(string)
  default     = {}
}
