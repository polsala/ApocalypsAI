variable "environment" {
  description = "Environment name (e.g., test, staging, prod)"
  type        = string
  default     = "test"
}

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "chaos_level" {
  description = "Chaos level for the garden (low, medium, high)"
  type        = string
  default     = "medium"
  validation {
    condition     = contains(["low", "medium", "high"], var.chaos_level)
    error_message = "Chaos level must be one of: low, medium, high."
  }
}

variable "vpc_cidr_block" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "create_ec2_instances" {
  description = "Whether to create EC2 instances"
  type        = bool
  default     = true
}

variable "ec2_instance_count" {
  description = "Number of EC2 instances to create"
  type        = number
  default     = 3
  validation {
    condition     = var.ec2_instance_count >= 1 && var.ec2_instance_count <= 10
    error_message = "EC2 instance count must be between 1 and 10."
  }
}

variable "ec2_instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "create_s3_buckets" {
  description = "Whether to create S3 buckets"
  type        = bool
  default     = true
}

variable "s3_bucket_count" {
  description = "Number of S3 buckets to create"
  type        = number
  default     = 2
  validation {
    condition     = var.s3_bucket_count >= 1 && var.s3_bucket_count <= 10
    error_message = "S3 bucket count must be between 1 and 10."
  }
}

variable "create_rds_instances" {
  description = "Whether to create RDS instances"
  type        = bool
  default     = true
}

variable "rds_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "create_lambda_functions" {
  description = "Whether to create Lambda functions"
  type        = bool
  default     = true
}

variable "lambda_function_count" {
  description = "Number of Lambda functions to create"
  type        = number
  default     = 2
  validation {
    condition     = var.lambda_function_count >= 1 && var.lambda_function_count <= 10
    error_message = "Lambda function count must be between 1 and 10."
  }
}

variable "enable_random_failures" {
  description = "Enable random failure scenarios"
  type        = bool
  default     = true
}

variable "enable_resource_exhaustion" {
  description = "Enable resource exhaustion scenarios"
  type        = bool
  default     = false
}

variable "enable_network_partitions" {
  description = "Enable network partition scenarios"
  type        = bool
  default     = true
}
