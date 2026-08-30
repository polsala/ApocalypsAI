variable "bucket_name_prefix" {
  description = "Prefix for the bucket name"
  type        = string
  default     = "cryptic-wardrobe"
}

variable "allowed_role_arn" {
  description = "IAM Role ARN that is allowed to access the bucket"
  type        = string
}
