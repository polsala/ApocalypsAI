variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. A unique suffix will be appended."
  type        = string
}

variable "environment" {
  description = "The environment name (e.g., \"dev\", \"prod\") to include in the bucket name."
  type        = string
}

variable "tags" {
  description = "A map of tags to apply to the S3 bucket."
  type        = map(string)
  default     = {}
}
