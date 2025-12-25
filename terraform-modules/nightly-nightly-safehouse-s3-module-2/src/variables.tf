variable "bucket_name" {
  description = "Name of the S3 bucket to create"
  type        = string
}

variable "versioning" {
  description = "Enable versioning on the bucket"
  type        = bool
  default     = true
}

variable "expiration_days" {
  description = "Number of days after which objects expire"
  type        = number
  default     = 30
}
