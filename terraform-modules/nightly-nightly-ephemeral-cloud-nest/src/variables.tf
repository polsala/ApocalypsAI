variable "project_name" {
  description = "A unique name for the project/environment."
  type        = string
  default     = "ephemeral-nest"
}

variable "instance_type" {
  description = "EC2 instance type."
  type        = string
  default     = "t2.micro"
}

variable "ami_id" {
  description = "The AMI ID for the EC2 instance."
  type        = string
}

variable "ttl_hours" {
  description = "Time To Live for the resources in hours."
  type        = number
  default     = 1
}

variable "key_name" {
  description = "(Optional) EC2 Key Pair name for SSH access."
  type        = string
  default     = null
}

variable "vpc_cidr_block" {
  description = "CIDR block for the VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_cidr_block" {
  description = "CIDR block for the public subnet."
  type        = string
  default     = "10.0.1.0/24"
}

variable "availability_zone" {
  description = "The AWS Availability Zone to deploy resources into."
  type        = string
  default     = "us-east-1a"
}
