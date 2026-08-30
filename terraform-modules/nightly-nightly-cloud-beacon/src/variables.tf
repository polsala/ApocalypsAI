variable "bucket_name" {
  description = "The name for the S3 bucket that will host the static website content. Must be globally unique."
  type        = string
}

variable "domain_name" {
  description = "(Optional) The custom domain name to associate with the CloudFront distribution. Leave empty to use CloudFront's default domain."
  type        = string
  default     = ""
}

variable "zone_id" {
  description = "(Optional) The Route 53 Hosted Zone ID for the custom domain. Required if domain_name is set."
  type        = string
  default     = ""
}
