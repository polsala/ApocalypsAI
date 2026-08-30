variable "bucket_name" {
  description = "The name of the S3 bucket to create. Must be globally unique."
  type        = string
}

variable "environment" {
  description = "The environment tag for the bucket (e.g., 'prod', 'dev', 'wasteland')."
  type        = string
  default     = "wasteland"
}

variable "tags" {
  description = "A map of tags to assign to the bucket."
  type        = map(string)
  default     = {}
}

variable "glacier_transition_days" {
  description = "Number of days after which to transition objects to GLACIER storage class."
  type        = number
  default     = 30
}

variable "access_logging_bucket_name" {
  description = "Optional: The name of the S3 bucket where access logs should be stored. If null, logging is disabled."
  type        = list(string)
  default     = null
}
