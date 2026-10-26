variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. A unique suffix will be added."
  type        = string
}

variable "expiration_days" {
  description = "Number of days after which objects will be automatically deleted."
  type        = number
  default     = 30
}

variable "tags" {
  description = "A map of tags to assign to the bucket."
  type        = map(string)
  default     = {}
}

variable "acl" {
  description = "The canned ACL to apply to the bucket."
  type        = string
  default     = "private"
  validation {
    condition     = contains(["private", "public-read", "public-read-write", "aws-exec-read", "authenticated-read", "bucket-owner-read", "bucket-owner-full-control", "log-delivery-write"], var.acl)
    error_message = "Invalid ACL. Must be one of: private, public-read, public-read-write, aws-exec-read, authenticated-read, bucket-owner-read, bucket-owner-full-control, log-delivery-write."
  }
}
