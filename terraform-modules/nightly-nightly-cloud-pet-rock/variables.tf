variable "bucket_name_prefix" {
  description = "A unique prefix for the S3 bucket name. The full bucket name will be generated with a random suffix."
  type        = string
  default     = "apocalypsai-pet-rock"
}

variable "enable_website_hosting" {
  description = "Set to true to enable static website hosting for the S3 bucket."
  type        = bool
  default     = false
}

variable "aws_region" {
  description = "The AWS region to deploy the S3 bucket in."
  type        = string
  default     = "us-east-1"
}
