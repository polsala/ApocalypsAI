variable "safehouse_name" {
  description = "Name of the safe‑house directory"
  type        = string
  default     = "safehouse"
}

variable "supplies" {
  description = "List of supplies to generate files for"
  type        = list(string)
  default     = []
}
