variable "region" {
  description = "AWS region to deploy resources."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "A unique name for the project, used to prefix resource names."
  type        = string
}

variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name to ensure uniqueness."
  type        = string
  default     = "apocalypsai"
}
