variable "region" {
  description = "The AWS region to deploy the temporal outpost."
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "The EC2 instance type for the temporal outpost."
  type        = string
  default     = "t2.micro"
}

variable "ami" {
  description = "The AMI ID for the EC2 instance. IMPORTANT: Use a valid AMI for your region."
  type        = string
  default     = "ami-0abcdef1234567890" # Placeholder. Replace with a valid AMI.
}

variable "outpost_name" {
  description = "A name tag for the temporal outpost EC2 instance."
  type        = string
  default     = "temporal-outpost"
}

variable "self_destruct_after_minutes" {
  description = "The suggested duration (in minutes) after which the outpost should be dismantled."
  type        = number
  default     = 60
}
