variable "bucket_name_prefix" {
  description = "A unique prefix for the S3 bucket name. A random suffix will be added."
  type        = string
}

variable "content_message" {
  description = "The HTML content or message to display on the beacon's index.html page."
  type        = string
  default     = "Hello, survivor! The ApocalypsAI beacon is active."
}

variable "aws_region" {
  description = "The AWS region where resources will be deployed."
  type        = string
  default     = "us-east-1"
}
