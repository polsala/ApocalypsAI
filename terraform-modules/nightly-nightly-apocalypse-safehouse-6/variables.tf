variable "region" {
  description = "AWS region to deploy resources"
  type        = string
}

variable "safehouse_name" {
  description = "Base name for resources (lowercase, alphanumeric, hyphens)"
  type        = string
  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.safehouse_name))
    error_message = "safehouse_name must contain only lowercase letters, numbers, and hyphens."
  }
}
