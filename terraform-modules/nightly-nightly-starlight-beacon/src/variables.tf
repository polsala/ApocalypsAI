variable "bucket_name" {
  description = "The name of the S3 bucket to create for the static website."
  type        = string
}

variable "index_document" {
  description = "The default document for the website (e.g., index.html)."
  type        = string
  default     = "index.html"
}

variable "error_document" {
  description = "The error document for the website (e.g., error.html)."
  type        = string
  default     = "error.html"
}

variable "tags" {
  description = "A map of tags to assign to the resources."
  type        = map(string)
  default     = {}
}

variable "aliases" {
  description = "A list of CNAMEs (domain names) for the CloudFront distribution."
  type        = list(string)
  default     = []
}

variable "acm_certificate_arn" {
  description = "The ARN of an AWS Certificate Manager (ACM) certificate for custom domains. Required if aliases are provided."
  type        = string
  default     = null
}
