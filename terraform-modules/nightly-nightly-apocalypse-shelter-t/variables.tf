variable "bucket_name" {
  description = "Name of the S3 bucket (must be globally unique)"
  type        = string
}

variable "index_document" {
  description = "Index document for the bucket website"
  type        = string
  default     = "index.html"
}

variable "error_document" {
  description = "Custom error document for the bucket website"
  type        = string
  default     = "error.html"
}

variable "region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}
