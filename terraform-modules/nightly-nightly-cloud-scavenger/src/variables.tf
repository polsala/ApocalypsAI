variable "prefix" {
  description = "A prefix for all resource names to ensure uniqueness and identification."
  type        = string
  default     = "apocalypsai"
}

variable "region" {
  description = "The AWS region where resources will be provisioned."
  type        = string
  default     = "us-east-1"
}

variable "enable_s3_cache" {
  description = "Set to true to provision an S3 bucket for data caching."
  type        = bool
  default     = true
}

variable "enable_ec2_relay" {
  description = "Set to true to provision an EC2 instance for communication relay."
  type        = bool
  default     = true
}

variable "ec2_instance_type" {
  description = "The instance type for the EC2 relay node (e.g., t3.nano, t2.micro)."
  type        = string
  default     = "t3.nano"
}

variable "ec2_ami_id" {
  description = "The AMI ID for the EC2 relay node. Provide a suitable AMI for your chosen region."
  type        = string
  default     = "ami-0abcdef1234567890" # Placeholder, user should provide a valid one.
}

variable "ec2_key_name" {
  description = "The name of the EC2 Key Pair to associate with the relay node. Must exist in the target region."
  type        = string
  default     = "apocalypsai-keypair" # Placeholder, user should create this.
}
