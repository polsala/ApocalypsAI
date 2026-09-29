variable "bucket_name" {
  description = "Name of the S3 bucket to create"
  type        = string
}

variable "create_initial_object" {
  description = "Whether to create an initial supply‑cache object"
  type        = bool
  default     = true
}

variable "initial_content" {
  description = "Content of the initial supply‑cache object"
  type        = string
  default     = "Emergency supplies placeholder"
}
