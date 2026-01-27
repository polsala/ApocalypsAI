variable "bucket_name" {
  description = "The unique name for the S3 bucket beacon. This must be globally unique across all AWS S3 buckets."
  type        = string
}

variable "whisper_content" {
  description = "The whimsical message or 'whisper' to store in the beacon."
  type        = string
  default     = "Hello from the void. All systems nominal... for now."
}

variable "aws_region" {
  description = "The AWS region to deploy the beacon. This should match the region configured in the AWS provider."
  type        = string
  default     = "us-east-1"
}
