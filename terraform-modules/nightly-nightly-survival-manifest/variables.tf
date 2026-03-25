variable "items" {
  description = "Map of survival item names to quantities."
  type        = map(number)
  default = {
    water         = 10
    canned_food   = 20
    first_aid_kit = 1
    flashlight    = 2
  }
}
