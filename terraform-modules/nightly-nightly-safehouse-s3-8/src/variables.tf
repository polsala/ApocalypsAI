variable "bucket_name_prefix" {
  description = "Prefix for the S3 bucket name"
  type        = string
  default     = "safehouse"
}

variable "region" {
  description = "AWS region where the bucket will be created"
  type        = string
  default     = "us-east-1"
}

variable "supply_content" {
  description = "Content of the starter‑supply object"
  type        = string
  default     = "Emergency rations"
}
