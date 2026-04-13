variable "function_name" {
  description = "The name of the Lambda function"
  type        = string
}

variable "handler" {
  description = "Function entry point"
  type        = string
}

variable "runtime" {
  description = "Runtime environment"
  type        = string
}

variable "filename" {
  description = "Path to deployment package"
  type        = string
}

variable "timeout" {
  description = "Timeout in seconds"
  type        = number
  default     = 3
}

variable "memory_size" {
  description = "Memory allocated in MB"
  type        = number
  default     = 128
}
