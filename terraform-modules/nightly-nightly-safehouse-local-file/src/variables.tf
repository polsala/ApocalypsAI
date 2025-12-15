variable "file_path" {
  description = "Path where the safehouse log file will be created."
  type        = string
}

variable "content" {
  description = "Content written into the safehouse log."
  type        = string
  default     = "Safehouse initialized.\n"
}
