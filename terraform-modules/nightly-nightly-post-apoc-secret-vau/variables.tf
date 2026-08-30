variable "length" {
  description = "Length of the generated password"
  type        = number
  default     = 16
}

variable "special" {
  description = "Include special characters"
  type        = bool
  default     = true
}

variable "override_special" {
  description = "Set of special characters to use"
  type        = string
  default     = "!@#$%&*()-_=+[]{}<>?"
}
