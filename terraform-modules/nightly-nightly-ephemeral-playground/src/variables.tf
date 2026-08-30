variable "region" {
  description = "AWS region to deploy resources."
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type for the playground."
  type        = string
  default     = "t2.micro"
}

variable "ami_id" {
  description = "AMI ID for the EC2 instance (e.g., Amazon Linux 2 HVM)."
  type        = string
  default     = "ami-053b0d53c279acc90" # Amazon Linux 2 AMI (HVM), SSD Volume Type - us-east-1
}

variable "key_name" {
  description = "Name of the AWS Key Pair to use for SSH access."
  type        = string
}

variable "public_key_path" {
  description = "Path to the public key file (.pub) to create the AWS Key Pair."
  type        = string
}

variable "destroy_after_hours" {
  description = "Number of hours after which the playground should be considered for destruction."
  type        = number
  default     = 24
}
