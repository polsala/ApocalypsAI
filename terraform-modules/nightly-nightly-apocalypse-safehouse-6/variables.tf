variable "bucket_name" {
  description = "Name of the S3 bucket (must be globally unique)"
  type        = string
}

variable "region" {
  description = "AWS region for the bucket"
  type        = string
  default     = "us-east-1"
}

variable "create_supply" {
  description = "Whether to create an initial supply object"
  type        = bool
  default     = false
}

variable "supply_content" {
  description = "Content of the initial supply object"
  type        = string
  default     = ""
}
