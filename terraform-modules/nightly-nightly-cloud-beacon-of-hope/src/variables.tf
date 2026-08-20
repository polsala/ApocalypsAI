variable "project_name" {
  description = "A unique name for the project, used as a prefix for resources."
  type        = string
  default     = "apocalypsai"
}

variable "env" {
  description = "The environment (e.g., 'prod', 'dev', 'staging')."
  type        = string
  default     = "prod"
}

variable "index_document" {
  description = "The default document for the website (e.g., index.html)."
  type        = string
  default     = "index.html"
}

variable "error_document" {
  description = "The error document for the website (e.g., error.html)."
  type        = string
  default     = "error.html"
}
