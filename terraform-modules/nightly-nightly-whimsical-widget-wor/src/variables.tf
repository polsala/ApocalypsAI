variable "project_name" {
  description = "A unique name for your whimsical widget, used for resource tagging."
  type        = string
  default     = "whimsical-widget"
}

variable "aws_region" {
  description = "The AWS region where resources will be provisioned."
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "The EC2 instance type for your widget host."
  type        = string
  default     = "t2.micro"
}

variable "ami_id" {
  description = "The AMI ID for the EC2 instance. Must be a valid AMI for your region."
  type        = string
  # Mock rationale: Using a placeholder AMI for deterministic, offline testing.
  # In a real deployment, this would be replaced with a valid, region-specific AMI.
  default     = "ami-0abcdef1234567890"
}

variable "ssh_key_name" {
  description = "(Optional) The name of an existing EC2 key pair for SSH access."
  type        = string
  default     = null
}
