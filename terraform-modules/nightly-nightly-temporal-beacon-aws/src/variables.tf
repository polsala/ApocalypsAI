variable "beacon_name" {
  description = "A unique name for your temporal anomaly beacon."
  type        = string
  default     = "temporal-beacon"
}

variable "aws_region" {
  description = "The AWS region to deploy the beacon in."
  type        = string
  default     = "us-east-1"
}

variable "log_level" {
  description = "The logging level for the Lambda function."
  type        = string
  default     = "INFO"
  validation {
    condition     = contains(["DEBUG", "INFO", "WARNING", "ERROR"], upper(var.log_level))
    error_message = "Log level must be one of DEBUG, INFO, WARNING, ERROR."
  }
}
