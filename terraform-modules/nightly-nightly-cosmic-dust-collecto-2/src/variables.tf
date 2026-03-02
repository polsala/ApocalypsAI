variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. The full name will be generated."
  type        = string
}

variable "environment" {
  description = "The environment (e.g., dev, prod) to tag resources with."
  type        = string
  default     = "dev"
}

variable "tags" {
  description = "A map of additional tags to apply to the S3 bucket and CloudWatch Log Group."
  type        = map(string)
  default     = {}
}
