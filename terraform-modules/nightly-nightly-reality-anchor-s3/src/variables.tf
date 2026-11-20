variable "bucket_name_prefix" {
  description = "A unique prefix for the S3 bucket name. Terraform will append a random string."
  type        = string
  default     = "apocalypsai-reality-anchor-"
}

variable "tags" {
  description = "A map of tags to assign to the S3 bucket."
  type        = map(string)
  default = {
    Project     = "ApocalypsAI"
    Environment = "Production"
    ManagedBy   = "ApocalypsAI-Integrator"
    Purpose     = "RealityAnchor"
  }
}
