variable "bucket_name" {
  description = "Name of the S3 bucket (must be globally unique)."
  type        = string
}

variable "tags" {
  description = "A map of tags to assign to the bucket."
  type        = map(string)
  default     = {}
}
