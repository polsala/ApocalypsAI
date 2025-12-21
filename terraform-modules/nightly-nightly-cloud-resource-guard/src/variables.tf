variable "project_name" {
  description = "The name of the project to associate with these resources."
  type        = string
  default     = "apocalypsai"
}

variable "environment" {
  description = "The deployment environment (e.g., dev, staging, production)."
  type        = string
  default     = "production"
}

variable "budget_threshold" {
  description = "The maximum estimated monthly AWS charges (in USD) before the alarm triggers."
  type        = number
  default     = 100
}
