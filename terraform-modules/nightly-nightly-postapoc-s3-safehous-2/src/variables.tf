variable "bucket_name" {
  description = "Name of the S3 bucket (must be globally unique)."
  type        = string
}

variable "expiration_days" {
  description = "Number of days after which objects expire."
  type        = number
  default     = 30
}

variable "tags" {
  description = "Tags to apply to the bucket."
  type        = map(string)
  default     = {}
}

variable "region" {
  description = "AWS region."
  type        = string
  default     = "us-east-1"
}
