variable "bucket_name" {
  description = "Name of the S3 bucket (must be globally unique)"
  type        = string
}

variable "create_supply_file" {
  description = "Whether to create an initial supply‑cache.txt object"
  type        = bool
  default     = false
}

variable "tags" {
  description = "Tags to apply to the bucket"
  type        = map(string)
  default     = {}
}

variable "aws_region" {
  description = "AWS region to deploy the bucket"
  type        = string
  default     = "us-east-1"
}
