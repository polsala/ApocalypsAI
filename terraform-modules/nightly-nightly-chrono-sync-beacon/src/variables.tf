variable "aws_region" {
  description = "AWS region to deploy resources."
  type        = string
  default     = "us-east-1"
}

variable "vpc_id" {
  description = "The ID of the VPC where the Chrono-Sync Beacon will be deployed."
  type        = string
}

variable "subnet_id" {
  description = "The ID of the subnet where the Chrono-Sync Beacon EC2 instance will be launched."
  type        = string
}

variable "instance_type" {
  description = "The EC2 instance type for the Chrono-Sync Beacon."
  type        = string
  default     = "t2.micro"
}

variable "ami_id" {
  description = "The AMI ID for the EC2 instance. Must be Amazon Linux 2 compatible."
  type        = string
  default     = "ami-053b0d53ed77771ad" # Amazon Linux 2 AMI (HVM) - Kernel 5.10, SSD Volume Type, us-east-1
}

variable "key_name" {
  description = "The name of the EC2 Key Pair to allow SSH access to the instance (optional)."
  type        = string
  default     = null
}

variable "environment" {
  description = "A tag to identify the environment (e.g., 'dev', 'prod')."
  type        = string
  default     = "default"
}
