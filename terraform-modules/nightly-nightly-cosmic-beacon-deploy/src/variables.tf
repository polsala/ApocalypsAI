variable "aws_region" {
  description = "The AWS region to deploy resources in."
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type for the beacon."
  type        = string
  default     = "t3.micro"
}

variable "min_size" {
  description = "Minimum number of beacon instances."
  type        = number
  default     = 1
}

variable "max_size" {
  description = "Maximum number of beacon instances."
  type        = number
  default     = 3
}

variable "desired_capacity" {
  description = "Desired number of beacon instances."
  type        = number
  default     = 1
}

variable "ami_id" {
  description = "The AMI ID for the EC2 instances. Defaults to latest Amazon Linux 2023 (us-east-1)."
  type        = string
  default     = "ami-053b0d534c2791404" # Amazon Linux 2023 (us-east-1, x86_64)
}
