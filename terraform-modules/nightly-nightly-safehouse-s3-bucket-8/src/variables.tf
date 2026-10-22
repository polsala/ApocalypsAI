variable "bucket_name_prefix" {
  description = "Prefix for the bucket name."
  type        = string
}

variable "tags" {
  description = "Tags to apply to the bucket."
  type        = map(string)
  default     = {}
}
