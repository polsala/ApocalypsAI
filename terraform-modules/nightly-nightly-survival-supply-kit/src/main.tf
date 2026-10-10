variable "supply_type" {
  description = "Type of supplies to retrieve"
  type        = string
  default     = "water"
}

locals {
  supplies = {
    water    = ["bottled water", "water filter"]
    food     = ["canned beans", "energy bars"]
    medicine = ["first aid kit", "pain relievers"]
  }
}

output "items" {
  description = "List of recommended items for the chosen supply type"
  value       = lookup(local.supplies, var.supply_type, [])
}
