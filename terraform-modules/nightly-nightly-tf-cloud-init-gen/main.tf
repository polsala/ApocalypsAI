locals {
  whimsical_suffixes = [
    "Scavenger",
    "Wanderer",
    "Oracle",
    "Sentinel",
    "Nomad",
    "Guardian",
    "Echo",
    "Whisper",
    "Rift-Walker",
    "Void-Navigator"
  ]
  random_suffix = element(local.whimsical_suffixes, random_integer.suffix_index.result)
  full_server_name = "${var.server_name}-${local.random_suffix}"
}

resource "random_integer" "suffix_index" {
  min = 0
  max = length(local.whimsical_suffixes) - 1
}

output "user_data" {
  description = "The generated cloud-init user_data."
  value = templatefile("${path.module}/templates/cloud_init.sh.tpl", {
    server_name = local.full_server_name
    boot_script = var.boot_script
  })
}

variable "server_name" {
  description = "The base name for the server."
  type        = string
}

variable "boot_script" {
  description = "A shell script to execute on instance boot."
  type        = string
  default     = ""
}
