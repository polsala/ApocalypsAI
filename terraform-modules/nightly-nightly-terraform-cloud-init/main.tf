resource "template_file" "cloud_init_user_data" {
  template = file("${path.module}/cloud_init.yaml.tpl")

  vars = {
    instance_name    = var.instance_name
    ssh_port         = var.ssh_port
    secret_port      = var.secret_port
    admin_user       = var.admin_user
    admin_password   = var.admin_password
    random_motd_seed = random_string.motd_seed.result
    secret_command   = random_string.secret_command.result
  }
}

variable "instance_name" {
  description = "The name of the instance."
  type        = string
}

variable "ssh_port" {
  description = "The SSH port to open."
  type        = number
}

variable "secret_port" {
  description = "A whimsical port for a secret command."
  type        = number
}

variable "admin_user" {
  description = "The username for the admin user."
  type        = string
}

variable "admin_password" {
  description = "The password for the admin user."
  type        = string
}

output "user_data" {
  description = "The generated cloud-init user data."
  value       = template_file.cloud_init_user_data.rendered
}

resource "random_string" "motd_seed" {
  length  = 16
  special = false
  upper   = false
}

resource "random_string" "secret_command" {
  length  = 8
  special = false
  upper   = false
  numeric = false
}
