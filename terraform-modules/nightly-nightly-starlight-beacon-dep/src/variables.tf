variable "beacon_message" {
  description = "The message to be displayed on the beacon page."
  type        = string
  default     = "Hello, cosmic wanderer! The ApocalypsAI Integrator is online."
}

variable "bucket_name_prefix" {
  description = "A unique prefix for the S3 bucket name. A random suffix will be appended."
  type        = string
  default     = "apocalypsai-starlight-beacon"
}

variable "aws_region" {
  description = "The AWS region to deploy resources in."
  type        = string
  default     = "us-east-1"
}
