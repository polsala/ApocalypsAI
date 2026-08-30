variable "aws_region" {
  description = "The AWS region to deploy resources into."
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "The EC2 instance type."
  type        = string
  default     = "t2.micro"
}

variable "ami_id" {
  description = "The AMI ID for the EC2 instance. If not provided, it will fetch the latest Ubuntu 22.04 AMI."
  type        = string
  default     = null # Allow dynamic lookup if not set
}

variable "bucket_name_prefix" {
  description = "Prefix for the S3 bucket name. A random suffix will be added."
  type        = string
  default     = "ephemeral-chamber"
}

variable "tags" {
  description = "A map of tags to apply to all resources."
  type        = map(string)
  default     = {
    ManagedBy = "ApocalypsAI"
    Purpose   = "EphemeralCloudChamber"
  }
}
