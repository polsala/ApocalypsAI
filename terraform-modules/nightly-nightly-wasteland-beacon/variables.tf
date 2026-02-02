variable "region" {
  description = "AWS region to deploy resources into."
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type for the beacon."
  type        = string
  default     = "t2.micro"
}

variable "ami_id" {
  description = "AMI ID for the EC2 instance. E.g., for Amazon Linux 2 in us-east-1: ami-0abcdef1234567890"
  type        = string
}

variable "key_name" {
  description = "EC2 Key Pair name for SSH access."
  type        = string
}

variable "beacon_port" {
  description = "Custom TCP port for the beacon signal."
  type        = number
  default     = 8080
}

variable "tags" {
  description = "A map of tags to apply to all created resources."
  type        = map(string)
  default     = {}
}
