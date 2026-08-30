# variables.tf - Input variables for the module

variable "region" {
  description = "AWS region to deploy the critter in."
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "The EC2 instance type for the critter."
  type        = string
  default     = "t2.micro"
}

variable "ami_id" {
  description = "The AMI ID for the critter. Must be valid for the chosen region."
  type        = string
  # Example for us-east-1, Amazon Linux 2 (HVM), SSD Volume Type
  # Users should update this to a current, valid AMI for their region.
  default     = "ami-053b0d53c279acc90" # Amazon Linux 2 AMI (HVM) - Kernel 5.10, us-east-1, 2023-12-19
}

variable "name_prefix" {
  description = "Prefix for the critter's name tag."
  type        = string
  default     = "apocalypsai-ephemeral"
}

variable "additional_tags" {
  description = "Additional tags to apply to the critter."
  type        = map(string)
  default     = {}
}
