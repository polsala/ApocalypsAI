variable "project_name" {
  description = "A unique name for the project, used as a prefix for resources."
  type        = string
  default     = "apocalypsai-whisper"
}

variable "bucket_name" {
  description = "The name for the S3 bucket hosting the static website. Must be globally unique."
  type        = string
  default     = "apocalypsai-whispering-post-bucket"
}

variable "dynamodb_table_name" {
  description = "The name for the DynamoDB table storing whispers."
  type        = string
  default     = "ApocalypsAIWhispers"
}

variable "whisper_ttl_hours" {
  description = "Time-to-live for whispers in hours. After this period, whispers are automatically deleted."
  type        = number
  default     = 24
}
