variable "bucket_name_prefix" {
  description = "A unique prefix for the S3 bucket name. A random suffix will be added."
  type        = string
  default     = "apocalypsai-beacon"
}

variable "content_file_path" {
  description = "Path to the HTML file to upload as the beacon's content. Relative to the module's root."
  type        = string
  default     = "beacon_message.html"
}

variable "region" {
  description = "The AWS region where the S3 bucket and CloudFront distribution will be created."
  type        = string
  default     = "us-east-1"
}
