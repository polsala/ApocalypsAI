variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. A random suffix will be appended."
  type        = string
}

variable "message_retention_days" {
  description = "Number of days after which messages (objects) in the bucket are deleted."
  type        = number
  default     = 30
}

variable "tags" {
  description = "A map of tags to assign to the S3 bucket."
  type        = map(string)
  default     = {}
}
