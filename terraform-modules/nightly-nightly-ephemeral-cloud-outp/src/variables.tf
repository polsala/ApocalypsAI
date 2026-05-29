variable "instance_name" {
  description = "Name tag for the EC2 instance."
  type        = string
  default     = "ephemeral-outpost"
}

variable "instance_type" {
  description = "The EC2 instance type."
  type        = string
  default     = "t2.micro"
}

variable "ami_id" {
  description = "The AMI ID for the EC2 instance."
  type        = string
}

variable "key_name" {
  description = "The name for the generated SSH key pair."
  type        = string
  default     = "ephemeral-key"
}

variable "ingress_ports" {
  description = "List of ports to allow ingress from anywhere (0.0.0.0/0)."
  type        = list(number)
  default     = [22]
}

variable "region" {
  description = "AWS region to deploy resources into."
  type        = string
  default     = "us-east-1"
}
