variable "aws_region" {
  description = "AWS region where the bucket will be created."
  type        = string
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "Optional bucket name; if empty a random name will be generated."
  type        = string
  default     = ""
}
