variable "bucket_name" {
  description = "The unique name for your S3 Chrono-Vault bucket."
  type        = string
}

variable "temporal_stasis_days" {
  description = "Number of days after which objects in the Chrono-Vault will enter 'temporal stasis' (transition to GLACIER storage class)."
  type        = number
  default     = 30 # Default to 30 days for stasis
}

variable "entropic_decay_days" {
  description = "Optional: Number of days after which objects in the Chrono-Vault will undergo 'entropic decay' (permanent deletion). If null, objects will remain in GLACIER indefinitely."
  type        = number
  default     = null
}

variable "tags" {
  description = "A map of tags to assign to the Chrono-Vault bucket."
  type        = map(string)
  default     = {}
}
