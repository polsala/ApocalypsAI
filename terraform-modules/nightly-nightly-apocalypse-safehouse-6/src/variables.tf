variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "allowed_role_arn" {
  description = "ARN of the IAM role to grant access"
  type        = string
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}
