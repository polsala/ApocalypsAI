# Mock rationale: This test configuration uses the module locally and relies on
# Terraform's plan output to verify logic, without provisioning actual cloud resources.
# The 'null_resource' is a common pattern to ensure a provider is initialized if
# the module itself doesn't directly use one, but for this module, it's not strictly
# necessary as it only processes inputs and generates outputs.
# We'll rely on the 'test.sh' script to assert outputs from 'terraform plan -json'.

module "test_constellation" {
  source = "../src" # Path to the module under test
  
  constellation_name = var.test_constellation_name
  environment        = var.test_environment
  additional_tags    = var.test_additional_tags
}
