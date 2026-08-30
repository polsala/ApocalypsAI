variable "beacon_message" {
  description = "The message to display on the static beacon page."
  type        = string
  default     = "All Clear. Stay Vigilant."
}

variable "aws_region" {
  description = "The AWS region where resources will be deployed."
  type        = string
  default     = "us-east-1"
}

variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name to ensure uniqueness."
  type        = string
  default     = "apocalypsai-beacon"
}
