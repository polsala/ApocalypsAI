variable "constellation_name" {
  description = "The whimsical name for your cloud constellation (e.g., \"Orion\", \"Pegasus\")."
  type        = string
}

variable "environment" {
  description = "The environment this constellation belongs to (e.g., \"dev\", \"prod\", \"staging\")."
  type        = string
}

variable "additional_tags" {
  description = "A map of additional tags to merge with the default constellation tags."
  type        = map(string)
  default     = {}
}
