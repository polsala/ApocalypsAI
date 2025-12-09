variable "garden_name" {
  description = "Name of the garden"
  type        = string
  default     = "void-garden"
}

variable "environment" {
  description = "Environment tag"
  type        = string
  default     = "dev"
}

variable "max_instances" {
  description = "Maximum number of instances"
  type        = number
  default     = 3
}

variable "min_instances" {
  description = "Minimum number of instances"
  type        = number
  default     = 1
}

variable "desired_capacity" {
  description = "Desired number of instances"
  type        = number
  default     = 2
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "easter_egg_path" {
  description = "Path to the hidden easter egg"
  type        = string
  default     = "/whimsical-void"
}

variable "key_name" {
  description = "Name of the SSH key pair"
  type        = string
  default     = ""
}
