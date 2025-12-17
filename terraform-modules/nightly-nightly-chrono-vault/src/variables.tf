variable "bucket_name" {
  description = "The name of the S3 bucket to create. Must be globally unique."
  type        = string
}

variable "encryption_algorithm" {
  description = "The server-side encryption algorithm to use. Can be 'AES256' or 'aws:kms'."
  type        = string
  default     = "AES256"
  validation {
    condition     = contains(["AES256", "aws:kms"], var.encryption_algorithm)
    error_message = "Encryption algorithm must be 'AES256' or 'aws:kms'."
  }
}

variable "kms_key_arn" {
  description = "The ARN of the KMS key to use if encryption_algorithm is 'aws:kms'."
  type        = string
  default     = null
}

variable "noncurrent_version_transition_days" {
  description = "Number of days after which noncurrent versions transition to GLACIER."
  type        = number
  default     = 30
}

variable "noncurrent_version_expiration_days" {
  description = "Number of days after which noncurrent versions expire."
  type        = number
  default     = 365
}

variable "tags" {
  description = "A map of tags to assign to the bucket."
  type        = map(string)
  default     = {}
}

variable "attach_policy" {
  description = "Whether to attach a default bucket policy (e.g., requiring TLS)."
  type        = bool
  default     = true
}

variable "enable_static_website" {
  description = "Whether to enable static website hosting for the bucket."
  type        = bool
  default     = false
}

variable "website_index_document" {
  description = "The name of the index document for static website hosting."
  type        = string
  default     = "index.html"
}

variable "website_error_document" {
  description = "The name of the error document for static website hosting."
  type        = string
  default     = "error.html"
}
