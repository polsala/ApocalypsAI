variable "enabled" {
  description = "Enable chaos monkey"
  type        = bool
  default     = false
}

variable "intensity" {
  description = "Probability (0-1) of destroying each resource"
  type        = number
  default     = 0.1
}

variable "resources" {
  description = "List of resource IDs to potentially destroy"
  type        = list(string)
  default     = []
}

variable "safe_mode" {
  description = "When true, only logs actions without destroying resources"
  type        = bool
  default     = true
}

variable "cloud_provider" {
  description = "Cloud provider (aws, gcp, azure)"
  type        = string
  default     = "aws"
}

variable "region" {
  description = "Cloud region for resources"
  type        = string
  default     = "us-east-1"
}
