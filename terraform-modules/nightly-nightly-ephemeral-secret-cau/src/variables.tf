variable "secret_name" {
  description = "The name of the ephemeral secret."
  type        = string
}

variable "secret_string" {
  description = "The actual secret value to store."
  type        = string
  sensitive   = true
}

variable "description" {
  description = "A description for the secret."
  type        = string
  default     = "An ephemeral secret managed by ApocalypsAI Nightly Integrator."
}

variable "recovery_window_in_days" {
  description = "The number of days that Secrets Manager will wait before permanently deleting the secret. Must be between 7 and 30. Set to 7 for maximum ephemerality."
  type        = number
  default     = 7
  validation {
    condition     = var.recovery_window_in_days >= 7 && var.recovery_window_in_days <= 30
    error_message = "The recovery_window_in_days must be between 7 and 30."
  }
}
