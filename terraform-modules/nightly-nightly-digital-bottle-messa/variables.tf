variable "project_name" {
  description = "A unique name for the project, used as a prefix for resources."
  type        = string
  default     = "apocalypsai"
}

variable "aws_region" {
  description = "The AWS region where resources will be deployed."
  type        = string
  default     = "us-east-1"
}
