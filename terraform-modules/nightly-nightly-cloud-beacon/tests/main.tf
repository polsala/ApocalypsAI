provider "aws" {
  region = "us-east-1"
  # Mock rationale: For terraform plan, AWS credentials are not strictly needed
  # if no remote state or backend is configured that requires them.
  # We are only testing the plan generation, not actual deployment.
  # Setting dummy values to satisfy provider requirements for plan.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
  token      = "mock_token"
}

provider "random" {} # Required by the module for unique bucket names

resource "random_string" "test_suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}

module "test_beacon" {
  source = "../src"

  beacon_message     = "Test Beacon Message for ApocalypsAI"
  aws_region         = "us-east-1"
  bucket_name_prefix = "test-apocalypsai-beacon-${random_string.test_suffix.result}"
}

output "test_website_endpoint" {
  value = module.test_beacon.website_endpoint
}
