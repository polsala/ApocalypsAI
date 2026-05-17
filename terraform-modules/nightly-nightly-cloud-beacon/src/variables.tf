variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. Must be globally unique."
  type        = string
  default     = "apocalypsai-beacon"
}

variable "region" {
  description = "The AWS region to deploy resources in."
  type        = string
  default     = "us-east-1"
}

variable "content_body" {
  description = "The main message to display on the beacon page."
  type        = string
  default     = "ApocalypsAI Beacon: We are here."
}

variable "tags" {
  description = "A map of tags to apply to all resources."
  type        = map(string)
  default     = {}
}
