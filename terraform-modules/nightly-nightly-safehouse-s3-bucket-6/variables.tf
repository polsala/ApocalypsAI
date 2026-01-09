variable "bucket_name" {
  description = "Name of the imagined S3 bucket"
  type        = string
  default     = "safehouse-bucket"
}

variable "versioning_enabled" {
  description = "Enable versioning on the bucket"
  type        = bool
  default     = true
}

variable "encryption_enabled" {
  description = "Enable server‑side encryption on the bucket"
  type        = bool
  default     = true
}

variable "lifecycle_days" {
  description = "Number of days after which objects are deleted"
  type        = number
  default     = 30
}
