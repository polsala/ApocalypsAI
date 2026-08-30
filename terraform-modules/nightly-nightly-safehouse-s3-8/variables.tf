variable "bucket_name" {
  description = "Name of the S3 bucket (must be globally unique)"
  type        = string
}

variable "allowed_role_arn" {
  description = "ARN of the IAM role that will receive read/write permissions"
  type        = string
}

variable "expiration_days" {
  description = "Number of days after which objects are deleted"
  type        = number
  default     = 30
}
