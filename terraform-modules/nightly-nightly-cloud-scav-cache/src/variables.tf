variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. Terraform will append a unique suffix."
  type        = string
  default     = "apocalypsai-scavenger-cache"
}

variable "tags" {
  description = "A map of tags to assign to the S3 bucket."
  type        = map(string)
  default = {
    Project     = "ApocalypsAI"
    Environment = "production"
    ManagedBy   = "ApocalypsAI-Integrator"
  }
}
