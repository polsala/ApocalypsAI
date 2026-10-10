variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. A random suffix will be appended for uniqueness."
  type        = string
  default     = "temporal-echo-vault"
}

variable "tags" {
  description = "A map of tags to assign to the S3 bucket."
  type        = map(string)
  default     = {}
}
