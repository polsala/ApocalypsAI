variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "enable_public_access_block" {
  description = "Whether to block public ACLs and policies"
  type        = bool
  default     = true
}
