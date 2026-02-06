variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. The full name will be generated as \"<prefix>-<environment>-apocalypsai\"."
  type        = string
  default     = "doomsday-bunker"
}

variable "environment" {
  description = "The environment name (e.g., prod, dev) to be included in the bucket name."
  type        = string
  default     = "prod"
}

variable "tags" {
  description = "A map of tags to assign to the S3 bucket."
  type        = map(string)
  default     = {}
}
