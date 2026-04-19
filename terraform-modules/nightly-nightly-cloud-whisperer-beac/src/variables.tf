variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. A unique suffix will be appended."
  type        = string
  default     = "apocalypsai-beacon"
}

variable "region" {
  description = "The AWS region where the S3 bucket will be created."
  type        = string
  default     = "us-east-1"
}

variable "content_path" {
  description = "The local path to the directory containing the static website content."
  type        = string
  default     = "src/content"
}
