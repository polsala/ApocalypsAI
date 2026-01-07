variable "bucket_name" {
  description = "Name of the S3 bucket (must be globally unique)"
  type        = string
}

variable "tags" {
  description = "Map of tags to assign to the bucket"
  type        = map(string)
  default     = {}
}

variable "lifecycle_days" {
  description = "Days after which objects transition to Glacier"
  type        = number
  default     = 30
}

variable "password_length" {
  description = "Length of the generated random password"
  type        = number
  default     = 16
}
