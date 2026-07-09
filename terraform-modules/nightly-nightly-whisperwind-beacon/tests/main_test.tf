# This file is for testing purposes only, demonstrating how the module would be called.
# It is not directly executed by the test_module.sh script, which focuses on
# validating the module's internal HCL.

provider "aws" {
  region = "us-east-1"
  # Mock rationale: For testing, we don't actually need to apply.
  # This provider block is here for terraform validate to understand the context.
  # In a real test run (e.g., with terratest), credentials would be provided.
}

module "test_beacon" {
  source = "../src" # Relative path to the module source

  region          = "us-east-1"
  instance_type   = "t2.micro"
  ami_id          = "ami-0abcdef1234567890" # Placeholder, replace with a valid test AMI
  key_name        = "test-key-pair"        # Placeholder, replace with a valid test key pair
  beacon_message  = "Test message from the void."
  beacon_port     = 8080
  tags = {
    Environment = "Test"
    Service     = "WhisperwindBeacon"
  }
}

output "test_public_ip" {
  value = module.test_beacon.public_ip
}

output "test_s3_bucket_name" {
  value = module.test_beacon.s3_bucket_name
}
