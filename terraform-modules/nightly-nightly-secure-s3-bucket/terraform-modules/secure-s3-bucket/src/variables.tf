variable "bucket_prefix" {
  description = "Prefix for the bucket name"
  type        = string
  default     = "apocalypse"
}

variable "tags" {
  description = "Tags to apply to the bucket"
  type        = map(string)
  default     = {}
}

variable "aws_region" {
  description = "AWS region for the provider"
  type        = string
  default     = "us-east-1"
}
