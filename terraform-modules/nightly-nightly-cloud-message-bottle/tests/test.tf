# Mock rationale: This test configuration uses the module and runs 'terraform plan'
# to verify the module's syntax and expected resource creation without
# actually provisioning AWS resources. The AWS provider is configured minimally
# to allow 'terraform init' and 'terraform plan' to succeed without
# requiring actual credentials for the plan phase.

provider "aws" {
  region = "us-east-1" # A default region is needed for the provider, but no actual API calls are made during 'plan'.
}

module "test_message_bottle" {
  source = "../src" # Path to the module under test

  bucket_name_prefix = "test-apocalypsai-bottle"
  expiration_days    = 2 # Test with 2 days expiration
  tags = {
    TestEnv = "True"
    Module  = "CloudMessageBottle"
  }
}

output "test_bucket_id" {
  value = module.test_message_bottle.bucket_id
}

output "test_bucket_arn" {
  value = module.test_message_bottle.bucket_arn
}

output "test_bucket_domain_name" {
  value = module.test_message_bottle.bucket_domain_name
}
