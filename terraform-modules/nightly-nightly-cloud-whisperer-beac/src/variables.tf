variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. A random suffix will be appended."
  type        = string
  default     = "apocalypsai-whisper-beacon"
}

variable "region" {
  description = "The AWS region to deploy the S3 bucket in."
  type        = string
  default     = "us-east-1"
}

variable "initial_whisper_message" {
  description = "The initial whimsical message to display on the beacon's index page."
  type        = string
  default     = "Greetings, wanderer! May your path be ever-illuminated by the glow of forgotten stars."
}
