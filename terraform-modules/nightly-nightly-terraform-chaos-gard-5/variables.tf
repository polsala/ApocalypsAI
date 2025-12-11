# General Configuration
variable "garden_name" {
  description = "Name prefix for all chaos garden resources"
  type        = string
  default     = "chaos-garden"
}

variable "aws_region" {
  description = "AWS region to deploy the chaos garden"
  type        = string
  default     = "us-east-1"
}

variable "sns_topic_arn" {
  description = "SNS topic ARN for alarm notifications (optional)"
  type        = string
  default     = ""
}

# Resource Creation Flags
variable "create_ec2_instances" {
  description = "Whether to create EC2 instances in the chaos garden"
  type        = bool
  default     = true
}

variable "ec2_instance_count" {
  description = "Number of EC2 instances to create"
  type        = number
  default     = 3
}

variable "create_lambda_functions" {
  description = "Whether to create Lambda functions for chaos experiments"
  type        = bool
  default     = true
}

variable "lambda_function_count" {
  description = "Number of Lambda functions to create"
  type        = number
  default     = 2
}

variable "create_s3_buckets" {
  description = "Whether to create S3 buckets in the chaos garden"
  type        = bool
  default     = true
}

variable "s3_bucket_count" {
  description = "Number of S3 buckets to create"
  type        = number
  default     = 2
}

variable "create_rds_instances" {
  description = "Whether to create RDS instances in the chaos garden"
  type        = bool
  default     = true
}

variable "rds_instance_count" {
  description = "Number of RDS instances to create"
  type        = number
  default     = 1
}

# Chaos Configuration
variable "enable_chaos_experiments" {
  description = "Whether to enable chaos experiments"
  type        = bool
  default     = true
}

variable "chaos_schedule" {
  description = "Schedule for chaos experiments (cron expression)"
  type        = string
  default     = "cron(0 */6 * * ? *)"
}

# Cleanup Configuration
variable "enable_automatic_cleanup" {
  description = "Whether to enable automatic cleanup of resources"
  type        = bool
  default     = true
}

variable "cleanup_schedule" {
  description = "Schedule for cleanup jobs (cron expression)"
  type        = string
  default     = "cron(0 3 * * ? *)"
}

# Monitoring Configuration
variable "enable_cloudwatch_dashboard" {
  description = "Whether to create a CloudWatch dashboard for monitoring"
  type        = bool
  default     = true
}

variable "enable_alarms" {
  description = "Whether to create CloudWatch alarms"
  type        = bool
  default     = true
}
