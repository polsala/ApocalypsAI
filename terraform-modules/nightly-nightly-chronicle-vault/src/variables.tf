variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. A random suffix will be appended."
  type        = string
  default     = "chronicle-vault"
}

variable "tags" {
  description = "A map of tags to assign to the S3 bucket."
  type        = map(string)
  default     = {}
}

variable "glacier_transition_days" {
  description = "Number of days after which noncurrent versions transition to Glacier Deep Archive."
  type        = number
  default     = 365
}

variable "multipart_upload_expiration_days" {
  description = "Number of days after which incomplete multipart uploads expire."
  type        = number
  default     = 7
}
