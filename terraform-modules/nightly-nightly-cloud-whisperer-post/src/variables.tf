variable "bucket_name_prefix" {
  description = "Prefix for the S3 bucket name. A unique suffix will be added."
  type        = string
  default     = "apocalypsai-whisper-postbox-"
}

variable "sns_topic_name" {
  description = "Name for the SNS topic."
  type        = string
  default     = "apocalypsai-whisper-channel"
}

variable "notification_filter_prefix" {
  description = "S3 object key prefix to filter notifications. Set to empty string for no prefix filter."
  type        = string
  default     = ""
}

variable "notification_filter_suffix" {
  description = "S3 object key suffix to filter notifications. Set to empty string for no suffix filter."
  type        = string
  default     = ""
}

variable "tags" {
  description = "A map of tags to assign to the resources."
  type        = map(string)
  default     = {}
}
