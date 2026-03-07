variable "bucket_name" {
  description = "The name of the S3 bucket for the Temporal Data Vault."
  type        = string
  default     = "apocalypsai-temporal-data-vault"
}

variable "tags" {
  description = "A map of tags to assign to the bucket."
  type        = map(string)
  default = {
    Project     = "ApocalypsAI"
    ManagedBy   = "NightlyIntegrator"
    Purpose     = "TemporalDataVault"
  }
}

variable "region" {
  description = "AWS region where the bucket will be created."
  type        = string
  default     = "us-east-1" # Default to a common region
}
