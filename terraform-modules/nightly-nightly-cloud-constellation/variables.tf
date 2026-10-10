variable "aws_region" {
  description = "The AWS region to deploy resources into."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "A unique name for your project, used for resource naming and tagging."
  type        = string
  default     = "apocalypsai"
}

variable "environment" {
  description = "The environment name (e.g., 'dev', 'prod') for tagging."
  type        = string
  default     = "development"
}

variable "project_tag_key" {
  description = "The tag key used to identify projects for constellation grouping."
  type        = string
  default     = "Project"
}

variable "environment_tag_key" {
  description = "The tag key used to identify environments for constellation grouping."
  type        = string
  default     = "Environment"
}

variable "scan_schedule_expression" {
  description = "The CloudWatch Event Rule schedule expression (e.g., 'cron(0 0 * * ? *)' for daily at midnight UTC)."
  type        = string
  default     = "cron(0 0 * * ? *)"
}
