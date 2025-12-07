variable "bunker_name_prefix" {
  description = "Prefix for the S3 bucket name. A random suffix will be added."
  type        = string
  default     = "apocalypsai-data-bunker"
}

variable "aws_region" {
  description = "AWS region to deploy the bunker in."
  type        = string
  default     = "us-east-1"
}

variable "tags" {
  description = "A map of tags to apply to all resources."
  type        = map(string)
  default     = {}
}
