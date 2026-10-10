variable "bucket_name" {
  description = "Name of the S3 bucket (must be globally unique)"
  type        = string
}

variable "tags" {
  description = "Map of tags to apply to the bucket"
  type        = map(string)
  default     = {}
}

variable "password_length" {
  description = "Length of the generated password"
  type        = number
  default     = 16
}

variable "password_special" {
  description = "Include special characters in the password"
  type        = bool
  default     = true
}
