variable "bucket_name" {
  description = "The name of the S3 bucket."
  type        = string
}

variable "region" {
  description = "The AWS region to deploy the S3 bucket in."
  type        = string
  default     = "us-east-1"
}

variable "enable_versioning" {
  description = "Whether to enable versioning for the S3 bucket."
  type        = bool
  default     = true
}

variable "enable_encryption" {
  description = "Whether to enable default server-side encryption (AES256) for the S3 bucket."
  type        = bool
  default     = true
}

variable "enable_public_access_block" {
  description = "Whether to enable public access block settings for the S3 bucket."
  type        = bool
  default     = true
}

variable "tags" {
  description = "A map of tags to assign to the S3 bucket."
  type        = map(string)
  default     = {}
}
