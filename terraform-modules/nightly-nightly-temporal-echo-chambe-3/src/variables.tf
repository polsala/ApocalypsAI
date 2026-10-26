variable "bucket_name" {
  description = "The name of the S3 bucket to create for the Temporal Echo Chamber."
  type        = string
}

variable "aws_region" {
  description = "The AWS region where the S3 bucket will be created."
  type        = string
  default     = "us-east-1"
}

variable "retention_days" {
  description = "Number of days after which noncurrent versions will transition to GLACIER storage class."
  type        = number
  default     = 90
}
