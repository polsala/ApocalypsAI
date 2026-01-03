variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "versioning" {
  description = "Enable versioning"
  type        = bool
  default     = true
}

variable "expiration_days" {
  description = "Days after which objects are deleted"
  type        = number
  default     = 30
}
