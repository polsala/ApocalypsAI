variable "bucket_name" {
  description = "The name for the S3 bucket (must be globally unique)."
  type        = string
}

variable "message_content" {
  description = "The initial message content to place in the bottle."
  type        = string
  default     = "Greetings, fellow survivors! May this message find you well. - ApocalypsAI"
}

variable "public_read" {
  description = "Set to true to make the bucket and its initial message publicly readable. Use with caution."
  type        = bool
  default     = true
}
