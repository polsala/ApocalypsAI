variable "bucket_name" {
  description = "Optional custom bucket name. Must be globally unique."
  type        = string
  default     = null
}

variable "region" {
  description = "AWS region where the bucket will be created."
  type        = string
  default     = "us-east-1"
}
