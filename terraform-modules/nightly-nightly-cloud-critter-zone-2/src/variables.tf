variable "project_name" {
  description = "The name of the project. Used for resource naming."
  type        = string
  default     = "apocalypsai"
}

variable "environment" {
  description = "The deployment environment. Used for resource naming."
  type        = string
  default     = "dev"
}

variable "critter_name" {
  description = "The name of your cloud critter. Used for resource naming."
  type        = string
  default     = "Whiskers"
}

variable "aws_region" {
  description = "The AWS region to deploy resources into."
  type        = string
  default     = "us-east-1"
}
