variable "bucket_name" {
  description = "The name of the S3 bucket to create."
  type        = string
}

variable "tags" {
  description = "A map of tags to assign to the bucket."
  type        = map(string)
  default     = {}
}
