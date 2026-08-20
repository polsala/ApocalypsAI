variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. A random suffix will be appended."
  type        = string
}

variable "domain_name" {
  description = "(Optional) The custom domain name for the CloudFront distribution. Requires the domain to be managed in Route 53."
  type        = string
  default     = null
}

variable "tags" {
  description = "A map of tags to assign to the resources."
  type        = map(string)
  default     = {}
}
