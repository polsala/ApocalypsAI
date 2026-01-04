variable "region" {
  description = "AWS region to deploy resources in."
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type."
  type        = string
  default     = "t2.micro"
}

variable "ami_id" {
  description = "AMI ID for the EC2 instance (Ubuntu 22.04 LTS)."
  type        = string
  default     = "ami-053b0d53d79c65660" # Ubuntu Server 22.04 LTS (HVM), SSD Volume Type in us-east-1
}

variable "key_name" {
  description = "Name of an existing EC2 Key Pair for SSH access."
  type        = string
  default     = ""
}

variable "tags" {
  description = "A map of tags to apply to all resources."
  type        = map(string)
  default     = {}
}
