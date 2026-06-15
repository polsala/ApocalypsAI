variable "bucket_name" {
  description = "The name of the S3 bucket. If empty, a random name will be generated."
  type        = string
  default     = ""
}

variable "retention_days" {
  description = "Number of days after which objects will expire."
  type        = number
  default     = 7
}

variable "tags" {
  description = "A map of tags to assign to the bucket."
  type        = map(string)
  default     = {}
}
