variable "bucket_prefix" {
  description = "Prefix for the bucket name"
  type        = string
  default     = "safehouse"
}

variable "tags" {
  description = "Tags to apply to the bucket"
  type        = map(string)
  default     = {}
}

variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}
