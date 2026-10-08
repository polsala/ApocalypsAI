variable "project_name" {
  description = "A unique name for the project, used as a prefix for resources."
  type        = string
}

variable "region" {
  description = "The AWS region to deploy the beacon."
  type        = string
  default     = "us-east-1"
}

variable "beacon_message" {
  description = "The message content to display on the static website beacon."
  type        = string
  default     = "ApocalypsAI Nightly Integrator Beacon: All systems nominal. Stay vigilant."
}

variable "index_document" {
  description = "The index document for the S3 static website."
  type        = string
  default     = "index.html"
}

variable "error_document" {
  description = "The error document for the S3 static website."
  type        = string
  default     = "error.html"
}
