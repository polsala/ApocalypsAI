# Test configuration for chaos orchestrator
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

# Test variables
variable "test_schedule" {
  type    = string
  default = "0 3 * * *"
}

variable "test_ttl" {
  type    = string
  default = "1h"
}

variable "test_max_resources" {
  type    = number
  default = 3
}

# Import the chaos orchestrator module
module "chaos_orchestrator" {
  source = "../"
  
  chaos_schedule  = var.test_schedule
  resource_ttl    = var.test_ttl
  max_resources   = var.test_max_resources
  providers       = ["aws", "gcp"]
  enable_chaos    = true
  resource_types  = ["instance", "bucket"]
}

# Test outputs
output "test_chaos_schedule" {
  value = module.chaos_orchestrator.chaos_schedule
}

output "test_resource_ttl" {
  value = module.chaos_orchestrator.resource_ttl
}

output "test_max_resources" {
  value = module.chaos_orchestrator.max_resources
}
