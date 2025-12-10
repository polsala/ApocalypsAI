variable "vault_name" {
  description = "The name for the cloud vault."
  type        = string
}

variable "region" {
  description = "The cloud region where the vault will be provisioned."
  type        = string
}

variable "rotation_enabled" {
  description = "Whether to enable automated secret rotation."
  type        = bool
  default     = false
}

variable "rotation_interval" {
  description = "The interval for secret rotation (e.g., \"12h\", \"7d\"). Required if rotation_enabled is true."
  type        = string
  default     = "720h" # 30 days
}

variable "secret_definitions" {
  description = "A map where keys are secret names and values are objects containing the secret value."
  type = map(object({
    value = string
  }))
  default = {}
}
