variable "garden_name" {
  description = "Name prefix for all resources"
  type        = string
  default     = "chaos-garden"
}

variable "chaos_factor" {
  description = "Probability (0.0-1.0) of resource destruction"
  type        = number
  default     = 0.2
}

variable "s3_buckets" {
  description = "List of S3 bucket names to create"
  type        = list(string)
  default     = ["flowers", "trees", "bushes"]
}

variable "dynamodb_tables" {
  description = "List of DynamoDB table names to create"
  type        = list(string)
  default     = ["insects", "birds", "soil"]
}

variable "lambda_functions" {
  description = "List of Lambda function names to create"
  type        = list(string)
  default     = ["watering", "pruning", "harvesting"]
}

variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}
