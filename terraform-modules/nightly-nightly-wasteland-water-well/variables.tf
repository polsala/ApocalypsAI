variable "well_name" {
  description = "Name of the water well"
  type        = string
  default     = "default-well"
}

variable "capacity_liters" {
  description = "Maximum water storage capacity in liters"
  type        = number
  default     = 1000
}

variable "alert_threshold" {
  description = "Water level threshold to trigger alerts"
  type        = number
  default     = 200
}
