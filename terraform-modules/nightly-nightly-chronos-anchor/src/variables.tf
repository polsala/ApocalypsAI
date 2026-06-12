variable "bucket_name" {
  description = "The name of the S3 bucket to create. Must be globally unique."
  type        = string
}

variable "region" {
  description = "The AWS region where the S3 bucket will be created."
  type        = string
  default     = "us-east-1"
}

variable "decay_days" {
  description = "Number of days after which the resource is considered for 'decay' (review/deletion)."
  type        = number
  default     = 90
}
