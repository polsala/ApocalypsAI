variable "bucket_name_prefix" {
  description = "Prefix for the S3 bucket name."
  type        = string
  default     = "apocalypse"
}

variable "tags" {
  description = "Tags to apply to the bucket."
  type        = map(string)
  default     = {}
}
