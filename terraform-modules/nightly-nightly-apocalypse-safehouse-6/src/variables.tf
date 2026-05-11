variable "bucket_name" {
  description = "Name of the S3 bucket."
  type        = string
}

variable "allowed_role_name" {
  description = "Name of the IAM role allowed to access the bucket."
  type        = string
}
