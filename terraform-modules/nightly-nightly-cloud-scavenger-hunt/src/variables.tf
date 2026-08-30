variable "prefix" {
  description = "A prefix for all resource names to ensure uniqueness."
  type        = string
  default     = "apocalypsai"
}

variable "region" {
  description = "AWS region to deploy resources into."
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type for the scavenger EC2."
  type        = string
  default     = "t2.micro"
}

variable "lambda_runtime" {
  description = "AWS Lambda runtime for the scavenger Lambda function."
  type        = string
  default     = "nodejs18.x"
}
