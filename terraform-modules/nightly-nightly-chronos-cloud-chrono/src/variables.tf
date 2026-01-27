variable "aws_region" {
  description = "The AWS region to deploy the NTP server in."
  type        = string
}

variable "vpc_id" {
  description = "The ID of the VPC where the NTP server will be deployed."
  type        = string
}

variable "subnet_id" {
  description = "The ID of the subnet where the NTP server EC2 instance will be launched."
  type        = string
}

variable "instance_type" {
  description = "The EC2 instance type for the NTP server."
  type        = string
  default     = "t2.micro"
}

variable "allowed_cidrs" {
  description = "A list of CIDR blocks that are allowed to access the NTP server (port 123 UDP)."
  type        = list(string)
}

variable "key_name" {
  description = "The name of an existing EC2 Key Pair to allow SSH access (optional)."
  type        = string
  default     = null
}

variable "tags" {
  description = "A map of tags to assign to the resources."
  type        = map(string)
  default     = {}
}
