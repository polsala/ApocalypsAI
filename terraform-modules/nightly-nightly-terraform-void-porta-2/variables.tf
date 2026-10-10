variable "portal_name" {
  description = "Human‑readable name for the portal"
  type        = string
  default     = "Void Portal"
}

variable "greeting" {
  description = "Optional greeting printed on apply"
  type        = string
  default     = null
}
