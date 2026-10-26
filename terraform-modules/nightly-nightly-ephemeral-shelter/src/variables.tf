variable "name_prefix" {
  description = "A unique prefix for all resources to avoid naming conflicts."
  type        = string
}

variable "region" {
  description = "AWS region to deploy resources into."
  type        = string
  default     = "us-east-1"
}

variable "ami_id" {
  description = "The AMI ID for the EC2 instance. Use a region-specific Amazon Linux 2 AMI."
  type        = string
  default     = "ami-053b0d53c279acc90" # Amazon Linux 2 AMI (HVM), SSD Volume Type - us-east-1
}

variable "instance_type" {
  description = "The EC2 instance type."
  type        = string
  default     = "t2.micro"
}

variable "create_key_pair" {
  description = "Whether to create a new SSH key pair for the instance. If false, `ssh_key_name` must be provided."
  type        = bool
  default     = true
}

variable "ssh_key_name" {
  description = "The name of an existing EC2 key pair to use. Required if `create_key_pair` is false."
  type        = string
  default     = null
}

variable "tags" {
  description = "A map of tags to assign to the EC2 instance."
  type        = map(string)
  default     = {}
}
