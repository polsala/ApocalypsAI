variable "region" {
  description = "AWS region to deploy resources"
  type        = string
}

variable "bucket_prefix" {
  description = "Prefix for the S3 bucket name"
  type        = string
  default     = "safehouse"
}
