variable "test_garden_name" {
  description = "Test garden name"
  type        = string
  default     = "test-chaos-garden"
}

variable "test_region" {
  description = "Test AWS region"
  type        = string
  default     = "us-west-2"
}

variable "test_chaos_level" {
  description = "Test chaos level"
  type        = number
  default     = 2
}

variable "test_enable_chaos" {
  description = "Test chaos enable flag"
  type        = bool
  default     = true
}
