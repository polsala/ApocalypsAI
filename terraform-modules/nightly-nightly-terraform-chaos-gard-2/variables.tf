variable "region" {
  description = "AWS region for the chaos garden"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment tag for resources"
  type        = string
  default     = "test"
}

variable "chaos_level" {
  description = "Level of chaos to introduce (low, medium, high)"
  type        = string
  default     = "medium"
  validation {
    condition     = contains(["low", "medium", "high"], var.chaos_level)
    error_message = "Chaos level must be one of: low, medium, high."
  }
}

variable "vpc_cidr" {
  description = "CIDR block for the chaos VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "enable_network_chaos" {
  description = "Enable network chaos resources"
  type        = bool
  default     = true
}

variable "enable_compute_chaos" {
  description = "Enable compute chaos resources"
  type        = bool
  default     = true
}

variable "enable_storage_chaos" {
  description = "Enable storage chaos resources"
  type        = bool
  default     = true
}

variable "instance_count" {
  description = "Number of EC2 instances to create"
  type        = number
  default     = 2
}

variable "instance_types" {
  description = "List of instance types for chaos instances"
  type        = list(string)
  default     = ["t3.micro", "t3.small", "t3.medium"]
}

variable "seed" {
  description = "Seed for random name generation"
  type        = number
  default     = 42
}

variable "notification_email" {
  description = "Email address for chaos notifications"
  type        = string
  default     = "chaos@example.com"
}

variable "destroy_after_hours" {
  description = "Auto-destroy resources after X hours (0 to disable)"
  type        = number
  default     = 0
}

variable "tags" {
  description = "Additional tags to apply to all resources"
  type        = map(string)
  default     = {}
}
