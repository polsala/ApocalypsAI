variable "ami_id" {
  description = "The AMI ID for the EC2 instance."
  type        = string
  default     = "ami-0abcdef1234567890" # Example, replace with a valid one for your region
}

variable "instance_type" {
  description = "The EC2 instance type."
  type        = string
  default     = "t2.micro"
}

variable "key_pair_name" {
  description = "The name of the EC2 Key Pair to allow SSH access."
  type        = string
}

variable "vpc_id" {
  description = "The ID of the VPC where the critter instance will be deployed."
  type        = string
}

variable "critter_name" {
  description = "A whimsical name for your cloud critter."
  type        = string
  default     = "Whimsy"
}
