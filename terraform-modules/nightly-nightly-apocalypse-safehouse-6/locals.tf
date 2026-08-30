resource "random_id" "id" {
  byte_length = 4
}

locals {
  default_bucket_name = "apocalypse-safehouse-${random_id.id.hex}"
}
