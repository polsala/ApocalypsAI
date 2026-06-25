variable "bucket_name" {
  description = "The name of the S3 bucket to create. Must be globally unique."
  type        = string
}

variable "bucket_acl" {
  description = "The ACL to apply to the bucket. Recommended: 'private'."
  type        = string
  default     = "private"
}

variable "noncurrent_transition_days" {
  description = "Number of days after which noncurrent versions transition to a different storage class."
  type        = number
  default     = 30
}

variable "noncurrent_transition_storage_class" {
  description = "The storage class to transition noncurrent versions to (e.g., GLACIER, STANDARD_IA)."
  type        = string
  default     = "STANDARD_IA"
}

variable "noncurrent_expiration_days" {
  description = "Number of days after which noncurrent versions expire and are permanently deleted."
  type        = number
  default     = 90
}

variable "tags" {
  description = "A map of tags to assign to the bucket."
  type        = map(string)
  default     = {}
}

variable "aws_region" {
  description = "The AWS region to deploy the S3 bucket in."
  type        = string
  default     = "us-east-1"
}
