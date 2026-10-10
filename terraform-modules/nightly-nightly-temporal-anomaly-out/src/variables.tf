variable "aws_region" {
  description = "AWS region to deploy resources into."
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type for the Temporal Anomaly Outpost."
  type        = string
  default     = "t2.micro"
}

variable "ami_id" {
  description = "AMI ID for the EC2 instance. Must be compatible with the chosen region."
  type        = string
}

variable "key_name" {
  description = "Name of the EC2 Key Pair for SSH access to the outpost."
  type        = string
}

variable "allowed_cidrs" {
  description = "List of CIDR blocks allowed to SSH into the outpost."
  type        = list(string)
  default     = ["0.0.0.0/0"] # WARNING: Broad access, restrict in production!
}

variable "outpost_name" {
  description = "Name tag for the EC2 instance and security group."
  type        = string
  default     = "TemporalAnomalyOutpost"
}
