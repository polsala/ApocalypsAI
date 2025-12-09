terraform {
  required_version = ">= 1.0"
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "random" {}

# Generate random security group name
resource "random_pet" "sg_name" {
  prefix = var.environment
}

# Generate random port ranges
resource "random_integer" "ssh_port" {
  min = 22
  max = 22
}

resource "random_integer" "http_port" {
  min = 80
  max = 80
}

resource "random_integer" "https_port" {
  min = 443
  max = 443
}

# Generate random priority
resource "random_integer" "priority" {
  min = 100
  max = 1000
}

# Create security group
resource "random_password" "sg_description" {
  length  = 64
  special = false
}

# Output the generated security group details
output "security_group_name" {
  value = random_pet.sg_name.id
}

output "ssh_port" {
  value = random_integer.ssh_port.result
}

output "http_port" {
  value = random_integer.http_port.result
}

output "https_port" {
  value = random_integer.https_port.result
}

output "priority" {
  value = random_integer.priority.result
}

output "description" {
  value = random_password.sg_description.result
}

output "allowed_ssh_cidrs" {
  value = var.allow_ssh_from
}

output "allowed_http_cidrs" {
  value = var.allow_http_from
}

output "allowed_https_cidrs" {
  value = var.allow_https_from
}
