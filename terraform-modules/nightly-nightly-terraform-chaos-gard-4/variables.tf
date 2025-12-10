variable "garden_name" {
  description = "Name for your chaos garden"
  type        = string
  default     = "chaos"
}

variable "region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-west-2"
}

variable "chaos_level" {
  description = "Level of chaos (1-5, higher means more chaos)"
  type        = number
  default     = 3
  validation {
    condition     = var.chaos_level >= 1 && var.chaos_level <= 5
    error_message = "Chaos level must be between 1 and 5."
  }
}

variable "enable_chaos" {
  description = "Enable chaos scenarios"
  type        = bool
  default     = true
}

variable "chaos_bucket_name" {
  description = "Optional specific name for the chaos S3 bucket"
  type        = string
  default     = null
}
