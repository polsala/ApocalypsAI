variable "bucket_name" {
  description = "Name of the S3 bucket (used for the JSON file name)"
  type        = string
}

variable "lifecycle_days" {
  description = "Number of days after which objects are considered expired"
  type        = number
  default     = 30
}
