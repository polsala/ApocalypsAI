variable "bucket_name_prefix" {
  description = "Optional prefix for the S3 bucket name. If empty, 'hide-seek' will be used."
  type        = string
  default     = ""
}

variable "common_tags" {
  description = "A map of common tags to apply to the bucket."
  type        = map(string)
  default     = {}
}
