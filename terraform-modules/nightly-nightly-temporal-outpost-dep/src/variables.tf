variable "name_prefix" {
  description = "A prefix for all resource names to ensure uniqueness."
  type        = string
  default     = "apocalypsai-temporal"
}

variable "aws_region" {
  description = "The AWS region to deploy resources into."
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "The environment tag for resources (e.g., 'dev', 'prod')."
  type        = string
  default     = "dev"
}

variable "schedule_expression" {
  description = "The CloudWatch/EventBridge schedule expression (e.g., 'rate(5 minutes)', 'cron(0 10 * * ? *)')."
  type        = string
  default     = "rate(15 minutes)"
}

variable "bucket_name" {
  description = "The name for the S3 bucket to store temporal logs. Must be globally unique."
  type        = string
  default     = "apocalypsai-temporal-outpost-logs-${random_id.bucket_suffix.hex}"
}
