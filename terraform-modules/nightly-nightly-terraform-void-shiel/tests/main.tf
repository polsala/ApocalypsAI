# Test configuration for nightly-terraform-void-shield

module "void_shield_test" {
  source = "../src"
  
  environment = "test"
  region      = "us-east-1"
  
  allow_ssh_from  = ["10.0.0.0/16", "192.168.0.0/16"]
  allow_http_from = ["0.0.0.0/0"]
  allow_https_from = ["0.0.0.0/0", "172.16.0.0/12"]
}

# Test outputs
output "test_security_group_name" {
  value = module.void_shield_test.security_group_name
}

output "test_ssh_port" {
  value = module.void_shield_test.ssh_port
}

output "test_http_port" {
  value = module.void_shield_test.http_port
}

output "test_https_port" {
  value = module.void_shield_test.https_port
}

output "test_priority" {
  value = module.void_shield_test.priority
}

output "test_description" {
  value = module.void_shield_test.description
}

output "test_allowed_ssh_cidrs" {
  value = module.void_shield_test.allowed_ssh_cidrs
}

output "test_allowed_http_cidrs" {
  value = module.void_shield_test.allowed_http_cidrs
}

output "test_allowed_https_cidrs" {
  value = module.void_shield_test.allowed_https_cidrs
}

output "test_security_group_rules" {
  value = module.void_shield_test.security_group_rules
}

output "test_module_info" {
  value = module.void_shield_test.module_info
}
