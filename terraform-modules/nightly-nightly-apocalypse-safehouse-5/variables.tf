variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "tags" {
  description = "Tags to apply to the bucket"
  type        = map(string)
  default     = {}
}

variable "create_initial_object" {
  description = "Whether to create a placeholder object"
  type        = bool
  default     = true
}

variable "initial_object_content" {
  description = "Content of the placeholder object"
  type        = string
  default     = "Emergency supplies inventory"
}
