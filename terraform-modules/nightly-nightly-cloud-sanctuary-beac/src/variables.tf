variable "aws_region" {
  description = "The AWS region to deploy the sanctuary beacon."
  type        = string
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "The name for the S3 bucket. Must be globally unique."
  type        = string
  default     = "apocalypsai-sanctuary-beacon-${random_id.bucket_suffix.hex}"
}

# To ensure unique bucket names
resource "random_id" "bucket_suffix" {
  byte_length = 8
}
