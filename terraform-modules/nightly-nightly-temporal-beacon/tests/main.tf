provider "aws" {
  region = "us-east-1"
  # Mock rationale: For testing, we don't need actual AWS credentials
  # as we are only running `terraform plan` and parsing its output.
  # The provider block is required for Terraform to validate syntax.
  # We'll use dummy credentials that won't be used for actual API calls.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "test_beacon" {
  source = "../src"
  
  region                     = "us-east-1"
  instance_type              = "t2.nano"
  ami_id                     = "ami-0abcdef1234567890" # A common dummy AMI ID
  beacon_name                = "TestTemporalAnchor"
  chronal_anchor_tag_value   = "TestTimelineStabilizer"
}

output "test_instance_id" {
  value = module.test_beacon.instance_id
}

output "test_public_ip" {
  value = module.test_beacon.public_ip
}
