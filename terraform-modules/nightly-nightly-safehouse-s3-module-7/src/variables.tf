variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "bucket_prefix" {
  description = "Prefix for bucket name"
  type        = string
  default     = "safehouse"
}

variable "lifecycle_days" {
  description = "Days after which non‑current versions are deleted"
  type        = number
  default     = 30
}
