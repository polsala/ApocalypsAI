variable "bucket_name" {
  description = "Name of the S3 bucket."
  type        = string
}

variable "iam_role_name" {
  description = "Name of the IAM role to attach the bucket policy."
  type        = string
}

variable "expiration_days" {
  description = "Number of days after which objects expire."
  type        = number
  default     = 30
}
