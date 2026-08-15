variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "bucket_prefix" {
  description = "Prefix for the bucket name"
  type        = string
  default     = "safehouse"
}

variable "expiration_days" {
  description = "Number of days after which objects expire"
  type        = number
  default     = 30
}
