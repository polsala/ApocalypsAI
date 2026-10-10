variable "bucket_name" {
  description = "The name of the S3 bucket for chrono-logs."
  type        = string
}

variable "environment" {
  description = "The environment tag for the S3 bucket (e.g., 'dev', 'prod')."
  type        = string
  default     = "dev"
}
