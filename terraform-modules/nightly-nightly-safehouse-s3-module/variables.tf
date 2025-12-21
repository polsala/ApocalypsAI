variable "bucket_name" {
  description = "Name of the S3 bucket."
  type        = string
}

variable "radiation_level" {
  description = "Radiation level tag for the bucket."
  type        = string
  default     = "moderate"
}
