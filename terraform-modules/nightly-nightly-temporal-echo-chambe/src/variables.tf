variable "aws_region" {
  description = "The AWS region to deploy resources into."
  type        = string
  default     = "us-east-1"
}

variable "ami_id" {
  description = "The AMI ID for the EC2 instance."
  type        = string
}

variable "instance_type" {
  description = "The EC2 instance type."
  type        = string
  default     = "t2.micro"
}

variable "duration_minutes" {
  description = "The duration in minutes after which the instance will self-terminate."
  type        = number
  default     = 60 # 1 hour
  validation {
    condition     = var.duration_minutes > 0
    error_message = "Duration must be greater than 0 minutes."
  }
}

variable "tags" {
  description = "A map of tags to apply to all resources."
  type        = map(string)
  default     = {}
}
