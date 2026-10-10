variable "test_constellation_name" {
  description = "Constellation name for testing."
  type        = string
}

variable "test_environment" {
  description = "Environment for testing."
  type        = string
}

variable "test_additional_tags" {
  description = "Additional tags for testing."
  type        = map(string)
  default     = {}
}
