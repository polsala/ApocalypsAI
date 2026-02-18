variable "bucket_name" {
  description = "The name of the S3 bucket for the static website. Must be globally unique."
  type        = string
}

variable "domain_name" {
  description = "The custom domain name for the CloudFront distribution (optional, for custom domains)."
  type        = string
  default     = ""
}

variable "index_document" {
  description = "The name of the index document (e.g., index.html)."
  type        = string
  default     = "index.html"
}

variable "error_document" {
  description = "The name of the error document (e.g., error.html)."
  type        = string
  default     = "error.html"
}

variable "aws_region" {
  description = "The AWS region to deploy resources into."
  type        = string
  default     = "us-east-1"
}
