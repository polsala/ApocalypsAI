# Mock rationale: This file is used by the test script to instantiate the module
# with mock inputs, allowing `terraform validate` and `terraform plan` to run
# without requiring actual cloud credentials or provisioning resources.
# It simulates a user's configuration.

module "test_chronos_bucket" {
  source = "../../src" # Relative path to the module under test
  
  bucket_name = "test-chronos-anchor-bucket-12345"
  region      = "us-east-1"
  decay_days  = 42
}
