variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. A unique suffix will be appended."
  type        = string
  default     = "anomaly-beacon"
}

variable "aws_region" {
  description = "The AWS region where the S3 bucket will be created."
  type        = string
}

variable "environment" {
  description = "An environment tag for the bucket (e.g., 'dev', 'prod')."
  type        = string
  default     = "dev"
}
