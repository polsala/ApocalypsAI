variable "project_name" {
  description = "A unique name for your project, used in resource tagging and naming."
  type        = string
  default     = "apocalypsai-beacon"
}

variable "aws_region" {
  description = "The AWS region to deploy resources in."
  type        = string
  default     = "us-east-1"
}

variable "content_bucket_name" {
  description = "The name for the S3 bucket that will host the beacon content. Must be globally unique."
  type        = string
  default     = "apocalypsai-whisperer-beacon-content-unique-name" # IMPORTANT: Change this to a globally unique name!
}
