variable "region" {
  description = "AWS region to deploy resources into."
  type        = string
  default     = "us-east-1"
}

variable "critter_name" {
  description = "A unique name for your digital critter."
  type        = string
  default     = "WhimsyCritter"
}

variable "instance_type" {
  description = "EC2 instance type for the critter habitat."
  type        = string
  default     = "t2.micro"
}

variable "ami_id" {
  description = "AMI ID for the EC2 instance. If empty, the latest Amazon Linux 2 AMI will be used."
  type        = string
  default     = ""
}

variable "key_name" {
  description = "The name of the EC2 Key Pair to allow SSH access."
  type        = string
  default     = "default-ssh-key"
}
