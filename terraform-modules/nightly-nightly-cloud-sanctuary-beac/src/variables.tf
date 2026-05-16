variable "project_name" {
  description = "A unique name for your project, used to prefix resource names."
  type        = string
  default     = "apocalypsai"
}

variable "environment" {
  description = "The deployment environment (e.g., dev, prod)."
  type        = string
  default     = "dev"
}

variable "content_file_path" {
  description = "Path to the local HTML file to upload as the beacon's content."
  type        = string
  default     = "${path.module}/content/index.html"
}
