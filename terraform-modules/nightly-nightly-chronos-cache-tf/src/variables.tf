variable "bucket_name_prefix" {
  description = "A unique prefix for the S3 bucket name. Terraform will append a unique suffix."
  type        = string
}

variable "expiration_days" {
  description = "Number of days after which objects (and non-current versions) in the bucket will be automatically deleted."
  type        = number
  default     = 7 # Default to 7 days
}

variable "tags" {
  description = "A map of tags to assign to the bucket."
  type        = map(string)
  default     = {}
}
