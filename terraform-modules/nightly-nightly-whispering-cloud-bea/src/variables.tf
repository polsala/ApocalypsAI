variable "bucket_name_prefix" {
  description = "A unique prefix for the S3 bucket name. The full name will be generated."
  type        = string
  default     = "apocalypsai-beacon"
}

variable "aws_region" {
  description = "The AWS region to deploy the beacon."
  type        = string
  default     = "us-east-1"
}

variable "beacon_message_html" {
  description = "The HTML content for the initial beacon message."
  type        = string
  default     = "<h1>Whispers of Hope from ApocalypsAI</h1><p>The signal lives on. Stay strong, survivors!</p>"
}

variable "index_document" {
  description = "The index document for the static website."
  type        = string
  default     = "index.html"
}
