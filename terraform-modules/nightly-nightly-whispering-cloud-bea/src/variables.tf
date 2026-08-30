variable "prefix" {
  description = "A unique prefix for all resources created by this module."
  type        = string
  default     = "beacon"
}

variable "memory_size" {
  description = "The amount of memory in MB your Lambda Function can use at runtime."
  type        = number
  default     = 128
}

variable "timeout" {
  description = "The amount of time your Lambda Function has to run in seconds."
  type        = number
  default     = 30
}

variable "runtime" {
  description = "The identifier of the function's runtime."
  type        = string
  default     = "python3.9"
}
