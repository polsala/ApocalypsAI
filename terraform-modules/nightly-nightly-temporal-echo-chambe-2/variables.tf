variable "project_name" {
  description = "The name of the project, used for resource naming."
  type        = string
  default     = "apocalypsai"
}

variable "environment" {
  description = "The deployment environment (e.g., dev, prod)."
  type        = string
  default     = "dev"
}

variable "region" {
  description = "The AWS region to deploy resources into."
  type        = string
  default     = "us-east-1"
}
