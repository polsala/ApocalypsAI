variable "bucket_name" {
  description = "Name of the S3 bucket."
  type        = string
}

variable "enable_secret" {
  description = "Create a random secret in Secrets Manager."
  type        = bool
  default     = false
}

variable "tags" {
  description = "Tags to apply to resources."
  type        = map(string)
  default     = {}
}
