variable "bucket_name" {
  description = "The name of the S3 bucket to create."
  type        = string
}

variable "region" {
  description = "The AWS region where the bucket will be deployed."
  type        = string
}

variable "tags" {
  description = "A map of tags to assign to the bucket."
  type        = map(string)
  default     = {}
}
