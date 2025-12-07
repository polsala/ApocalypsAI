variable "project_name" {
  description = "A unique name prefix for all resources to avoid conflicts."
  type        = string
  default     = "apocalypsai"
}

variable "aws_region" {
  description = "The AWS region to deploy resources into."
  type        = string
  default     = "us-east-1"
}
