variable "environment" {
  description = "The environment name (e.g., staging, production)"
  type        = string
  default     = "staging"
}

variable "region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-west-2"
}

variable "chaos_scenarios" {
  description = "List of chaos scenarios to enable"
  type        = list(string)
  default     = ["network_latency", "resource_deletion", "service_disruption"]
}

variable "max_concurrent_experiments" {
  description = "Maximum number of concurrent chaos experiments"
  type        = number
  default     = 3
}

variable "experiment_duration" {
  description = "Duration of each chaos experiment"
  type        = string
  default     = "30m"
}

variable "rollback_enabled" {
  description = "Enable automatic rollback for failed experiments"
  type        = bool
  default     = true
}

variable "enable_monitoring" {
  description = "Enable monitoring and alerting for chaos experiments"
  type        = bool
  default     = true
}

variable "alert_email" {
  description = "Email address for chaos experiment alerts"
  type        = string
  default     = ""
}

variable "tags" {
  description = "Additional tags to apply to resources"
  type        = map(string)
  default     = {}
}
