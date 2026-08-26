variable "region" {
  description = "AWS region where the bucket will be created"
  type        = string
}

variable "bucket_name" {
  description = "Globally unique bucket name"
  type        = string
}

variable "password_length" {
  description = "Length of the generated random password"
  type        = number
  default     = 16
}

variable "expiration_days" {
  description = "Number of days after which objects expire"
  type        = number
  default     = 365
}
