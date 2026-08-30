variable "name" {
  description = "Name of the security group"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID where the security group will be created"
  type        = string
}

variable "rule_count" {
  description = "Number of random ingress rules to create"
  type        = number
  default     = 1
}
