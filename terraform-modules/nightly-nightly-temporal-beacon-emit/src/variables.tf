variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. A unique suffix will be appended."
  type        = string
  default     = "apocalypsai-beacon"
}

variable "region" {
  description = "The AWS region where the S3 bucket will be created."
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "The environment tag for the S3 bucket."
  type        = string
  default     = "dev"
}
