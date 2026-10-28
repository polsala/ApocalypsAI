variable "queue_name" {
  description = "The name of the SQS queue."
  type        = string
  default     = "whisperwind-message-queue"
}

variable "topic_name" {
  description = "The name of the SNS topic."
  type        = string
  default     = "whisperwind-message-topic"
}

variable "queue_delay_seconds" {
  description = "The length of time, in seconds, for which the delivery of all messages in the queue is delayed."
  type        = number
  default     = 0
}

variable "queue_max_message_size" {
  description = "The limit of how many bytes a message can contain before Amazon SQS rejects it."
  type        = number
  default     = 262144 # 256 KB
}

variable "queue_message_retention_seconds" {
  description = "The number of seconds Amazon SQS retains a message."
  type        = number
  default     = 345600 # 4 days
}

variable "queue_receive_wait_time_seconds" {
  description = "The length of time, in seconds, for which a ReceiveMessage call will wait for a message to arrive."
  type        = number
  default     = 0
}

variable "queue_visibility_timeout_seconds" {
  description = "The duration (in seconds) that an item is hidden from other consumers after a consumer retrieves it."
  type        = number
  default     = 30
}

variable "tags" {
  description = "A map of tags to assign to the resources."
  type        = map(string)
  default     = {}
}
