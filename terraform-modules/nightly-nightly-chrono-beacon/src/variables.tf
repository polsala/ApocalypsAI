variable "region" {
  description = "AWS region to deploy resources in."
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type for the beacon application."
  type        = string
  default     = "t2.micro"
}

variable "vpc_id" {
  description = "The ID of the VPC where the beacon will be deployed."
  type        = string
}

variable "subnet_ids" {
  description = "A list of subnet IDs for the Auto Scaling Group and Load Balancer."
  type        = list(string)
}

variable "desired_capacity" {
  description = "The desired number of EC2 instances in the Auto Scaling Group."
  type        = number
  default     = 1
}

variable "min_size" {
  description = "The minimum number of EC2 instances in the Auto Scaling Group."
  type        = number
  default     = 1
}

variable "max_size" {
  description = "The maximum number of EC2 instances in the Auto Scaling Group."
  type        = number
  default     = 1
}

variable "ami_id" {
  description = "The AMI ID for the EC2 instances (e.g., Amazon Linux 2). If null, the latest Amazon Linux 2 AMI will be used."
  type        = string
  default     = null
}
