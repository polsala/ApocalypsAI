variable "bucket_name" {
  description = "Name of the safe‑house bucket."
  type        = string
}

variable "versioning" {
  description = "Enable versioning."
  type        = bool
  default     = true
}

variable "encryption" {
  description = "Server‑side encryption algorithm."
  type        = string
  default     = "AES256"
}

variable "retention_days" {
  description = "Lifecycle retention period in days."
  type        = number
  default     = 30
}
