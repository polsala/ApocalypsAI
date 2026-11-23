variable "filename" {
  description = "Name of the file to create"
  type        = string
}

variable "length" {
  description = "Length of the random string in bytes (will be hex‑encoded)"
  type        = number
  default     = 8
  validation {
    condition     = var.length > 0 && var.length <= 64
    error_message = "Length must be between 1 and 64 bytes."
  }
}
