variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. A random suffix will be appended."
  type        = string
  default     = "whisper-vault-"
}

variable "region" {
  description = "The AWS region where the S3 bucket will be created."
  type        = string
  default     = "us-east-1"
}

variable "retention_days" {
  description = "Number of days after which objects (and non-current versions) will be expired and deleted."
  type        = number
  default     = 7
}
