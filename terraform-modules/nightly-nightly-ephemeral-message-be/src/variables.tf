variable "bucket_prefix" {
  description = "A prefix for the S3 bucket name. The full name will be `prefix-randomstring`."
  type        = string
  default     = "apocalypsai-beacon"
}

variable "expiration_days" {
  description = "Number of days after which objects in the bucket will be automatically deleted."
  type        = number
  default     = 7
}

variable "aws_region" {
  description = "The AWS region where the S3 bucket will be created."
  type        = string
  default     = "us-east-1"
}
