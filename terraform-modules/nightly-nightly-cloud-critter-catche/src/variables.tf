variable "critter_name" {
  description = "A whimsical name for your cloud critter."
  type        = string
  default     = "ephemeral-critter"
}

variable "region" {
  description = "The AWS region to deploy the critter in."
  type        = string
  default     = "us-east-1"
}

variable "ami_id" {
  description = "The AMI ID for the critter instance. Must be valid for the chosen region."
  type        = string
  default     = "ami-053b0d534c279acc9" # Amazon Linux 2 AMI in us-east-1 (as of early 2023, might need update)
}

variable "instance_type" {
  description = "The EC2 instance type for the critter."
  type        = string
  default     = "t2.micro"
}

variable "lifespan_minutes" {
  description = "The number of minutes the critter will live before self-terminating."
  type        = number
  default     = 10
  validation {
    condition     = var.lifespan_minutes > 0
    error_message = "Lifespan must be greater than 0 minutes."
  }
}

variable "vpc_security_group_ids" {
  description = "List of security group IDs to associate with the instance."
  type        = list(string)
  default     = []
}

variable "subnet_id" {
  description = "The ID of the subnet to launch the instance into. If not provided, AWS chooses."
  type        = string
  default     = null
}
