# Test-specific variables
variable "test_schedule" {
  description = "Test cron schedule"
  type        = string
  default     = "0 3 * * *"
}

variable "test_ttl" {
  description = "Test resource TTL"
  type        = string
  default     = "1h"
}

variable "test_max_resources" {
  description = "Test maximum resources"
  type        = number
  default     = 3
}

variable "test_providers" {
  description = "Test cloud providers"
  type        = list(string)
  default     = ["aws", "gcp"]
}
