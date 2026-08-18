variable "relay_name" {
  description = "The name of the SQS queue (Whisperwind Relay)."
  type        = string
  default     = "whisperwind-relay"
}

variable "visibility_timeout_seconds" {
  description = "The duration (in seconds) that a message will be unavailable after a consumer retrieves it."
  type        = number
  default     = 30
}

variable "message_retention_seconds" {
  description = "The number of seconds Amazon SQS retains a message."
  type        = number
  default     = 345600 # 4 days
}

variable "delay_seconds" {
  description = "The length of time (in seconds) that the delivery of all messages in the queue will be delayed."
  type        = number
  default     = 0
}
