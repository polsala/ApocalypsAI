variable "bucket_name" {
  description = "The name of the S3 bucket for the wasteland cache vault."
  type        = string
}

variable "tags" {
  description = "A map of tags to assign to the bucket."
  type        = map(string)
  default     = {}
}

variable "retention_days_standard_to_ia" {
  description = "Number of days after which objects in STANDARD storage class are moved to STANDARD_IA."
  type        = number
  default     = 30
}

variable "retention_days_ia_to_glacier" {
  description = "Number of days after which objects in STANDARD_IA storage class are moved to GLACIER."
  type        = number
  default     = 90
}

variable "retention_days_glacier_to_delete" {
  description = "Number of days after which objects in GLACIER storage class are permanently deleted."
  type        = number
  default     = 365
}
