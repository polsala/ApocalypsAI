variable "instance_type" {
  description = "The EC2 instance type."
  type        = string
  default     = "t2.micro"
}

variable "ami_id" {
  description = "The AMI ID for the EC2 instance. You must provide a valid AMI ID for your AWS region."
  type        = string
}

variable "bucket_name" {
  description = "A unique name for the S3 bucket."
  type        = string
}
