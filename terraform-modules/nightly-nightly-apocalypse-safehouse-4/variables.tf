variable "bucket_name" {
  description = "Custom bucket name (must be globally unique). If null, a random name is generated."
  type        = string
  default     = null
}

variable "tags" {
  description = "A map of tags to assign to the bucket."
  type        = map(string)
  default     = {}
}
