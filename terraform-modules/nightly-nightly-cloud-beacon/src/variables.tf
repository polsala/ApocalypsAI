variable "bucket_name_prefix" {
  description = "Prefix for the S3 bucket name. A random suffix will be appended."
  type        = string
  default     = "apocalypsai-beacon"
}

variable "region" {
  description = "AWS region to deploy resources."
  type        = string
  default     = "us-east-1"
}

variable "message_seed" {
  description = "The core message or seed for the beacon's content."
  type        = string
  default     = "Hope flickers, but never dies."
}
