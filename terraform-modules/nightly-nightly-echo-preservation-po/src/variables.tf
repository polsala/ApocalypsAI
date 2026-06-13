variable "name_prefix" {
  description = "A unique prefix for the S3 bucket name."
  type        = string
  default     = "echo-preservation"
}

variable "environment" {
  description = "The environment tag for the bucket (e.g., dev, prod, staging)."
  type        = string
  default     = "dev"
}

variable "retention_days_standard" {
  description = "Number of days to keep objects in standard storage before moving to Glacier."
  type        = number
  default     = 30
}

variable "retention_days_glacier" {
  description = "Number of days to keep objects in Glacier before permanent deletion."
  type        = number
  default     = 365
}

variable "tags" {
  description = "A map of tags to assign to the S3 bucket."
  type        = map(string)
  default     = {}
}
