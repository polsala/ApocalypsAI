variable "resource_name_prefix" {
  description = "A prefix for the S3 bucket name to ensure uniqueness."
  type        = string
}

variable "region" {
  description = "The AWS region where the S3 bucket will be created."
  type        = string
}

variable "ttl_days" {
  description = "The number of days after which objects in the bucket will expire."
  type        = number
  default     = 7
}

variable "tags" {
  description = "A map of tags to apply to the S3 bucket."
  type        = map(string)
  default     = {}
}
