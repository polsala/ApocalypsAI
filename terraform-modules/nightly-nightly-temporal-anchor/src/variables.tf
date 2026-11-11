variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. Must be globally unique. A random suffix will be appended."
  type        = string
  default     = "apocalypsai"
}
