# tests/main.tf
# This file is used by `terraform test` to instantiate the module under test.
module "beacon_test" {
  source = "../src"
  prefix = "test-beacon" # Override default prefix for testing
}
