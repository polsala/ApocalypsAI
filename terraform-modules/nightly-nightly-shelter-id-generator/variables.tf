variable "shelter_name" {
  description = "Human‑readable name of the shelter"
  type        = string
  default     = "Unnamed Shelter"
}

variable "capacity" {
  description = "Maximum number of occupants"
  type        = number
  default     = 10
}

variable "id_length" {
  description = "Length of the random ID in bytes"
  type        = number
  default     = 8
}
