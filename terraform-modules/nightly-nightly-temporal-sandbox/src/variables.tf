variable "aws_region" {
  description = "The AWS region to deploy resources into."
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "The EC2 instance type for the sandbox."
  type        = string
  default     = "t2.micro"
}

variable "ttl_hours" {
  description = "Time-To-Live for the sandbox in hours."
  type        = number
  default     = 24
}

variable "sandbox_name" {
  description = "A unique name for this temporal sandbox."
  type        = string
  default     = "default-temporal-sandbox"
}
