# This file is used by the test script to validate the module.
# It instantiates the module with default values.

module "test_bunker" {
  source = "../src"

  bucket_name_prefix = "test-bunker"
  region             = "us-east-1"
  tags = {
    TestEnv = "True"
  }
}
