provider "template" {}

resource "random_string" "motd_seed_test" {
  length  = 16
  special = false
  upper   = false
}

resource "random_string" "secret_command_test" {
  length  = 8
  special = false
  upper   = false
  numeric = false
}

module "test_cloud_init" {
  source = ".."

  instance_name    = "test-instance"
  ssh_port         = 22
  secret_port      = 8080
  admin_user       = "testuser"
  admin_password   = "testpass"
}

output "rendered_user_data" {
  value = module.test_cloud_init.user_data
}

# Mock rationale: Using template_file and random_string resources directly for deterministic testing.
# The output of these resources is predictable given the inputs, allowing for direct assertion.
# No external services or complex state management are required.

output "contains_motd_header" {
  description = "Checks if the MOTD header is present."
  value       = can(regex("Welcome to the test-instance! Your secret handshake command is: ${random_string.secret_command_test.result}", module.test_cloud_init.user_data))
}

output "contains_secret_handshake_command" {
  description = "Checks if the secret handshake command script is present."
  value       = can(regex("echo \"#!/bin/bash\\nif [ \\\"$1\\\" = \\\"${random_string.secret_command_test.result}\\\" ]; then", module.test_cloud_init.user_data))
}

output "contains_ufw_rules" {
  description = "Checks if ufw rules for SSH and secret port are present."
  value       = can(regex("ufw allow 22/tcp\n  ufw allow 8080/tcp", module.test_cloud_init.user_data))
}

output "contains_admin_user_creation" {
  description = "Checks if admin user creation commands are present."
  value       = can(regex("useradd -m -s /bin/bash testuser\n  echo \"testuser:testpass\" | chpasswd", module.test_cloud_init.user_data))
}
