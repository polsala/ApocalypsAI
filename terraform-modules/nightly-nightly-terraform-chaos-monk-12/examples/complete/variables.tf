# Example Variables for Complete Chaos Monkey Setup

variable "aws_region" {
  description = "AWS region for the example"
  type        = string
  default     = "us-east-1"
}

variable "dry_run" {
  description = "Enable dry run mode for safety"
  type        = bool
  default     = true
}
