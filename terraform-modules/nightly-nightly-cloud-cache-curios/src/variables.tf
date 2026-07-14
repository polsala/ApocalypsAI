variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. A unique suffix will be appended."
  type        = string
  default     = "apocalypsai-curios"
}

variable "retention_days" {
  description = "Number of days after which objects in the bucket will be permanently deleted."
  type        = number
  default     = 365
}

variable "transition_to_ia_days" {
  description = "Number of days after which objects will transition to Infrequent Access."
  type        = number
  default     = 30
}

variable "tags" {
  description = "A map of tags to assign to the S3 bucket."
  type        = map(string)
  default     = {}
}
