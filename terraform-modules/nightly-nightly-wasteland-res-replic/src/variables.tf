variable "resource_type" {
  description = "The type of resource to replicate (e.g., 'survival_pod', 'data_cache')."
  type        = string
  default     = "survival_pod"
}

variable "resource_count" {
  description = "The desired number of replicated resources."
  type        = number
  default     = 3
  validation {
    condition     = var.resource_count > 0
    error_message = "The resource_count must be greater than 0."
  }
}
