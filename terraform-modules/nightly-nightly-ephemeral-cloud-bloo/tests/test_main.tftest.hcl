# Mock rationale: Terraform's native 'terraform test' framework allows for defining test configurations
# that instantiate modules and assert properties. By using `command = plan`, these tests validate the
# *planned* configuration and outputs without requiring actual AWS API calls to succeed or provisioning
# real infrastructure. This ensures the module's logic and variable processing are correct offline.

run "test_default_configuration" {
  command = plan

  module "test_bloom" {
    source = "../src"

    bucket_name_prefix = "test-bloom-prefix"
    expiration_days    = 7
    enable_public_access = false
  }

  assert {
    condition     = module.test_bloom.bucket_id == "test-bloom-prefix-ephemeral-cloud-bloom"
    error_message = "Bucket ID does not match expected format."
  }

  assert {
    condition     = module.test_bloom.bucket_arn == "arn:aws:s3:::test-bloom-prefix-ephemeral-cloud-bloom"
    error_message = "Bucket ARN does not match expected format."
  }

  assert {
    condition     = module.test_bloom.lifecycle_rule_id == "ephemeral-object-expiration"
    error_message = "Lifecycle rule ID does not match expected value."
  }
  assert {
    condition     = module.test_bloom.lifecycle_expiration_days == 7
    error_message = "Lifecycle expiration days do not match expected value."
  }
  assert {
    condition     = module.test_bloom.bucket_website_endpoint == null
    error_message = "Website endpoint should be null when public access is disabled."
  }
}

run "test_public_access_enabled" {
  command = plan

  module "public_bloom" {
    source = "../src"

    bucket_name_prefix = "public-test-bloom"
    expiration_days    = 1
    enable_public_access = true
  }

  assert {
    condition     = public_bloom.bucket_website_endpoint != null
    error_message = "Website endpoint should be available when public access is enabled."
  }
  assert {
    condition     = public_bloom.bucket_id == "public-test-bloom-ephemeral-cloud-bloom"
    error_message = "Public bucket ID does not match expected format."
  }
  assert {
    condition     = public_bloom.lifecycle_expiration_days == 1
    error_message = "Public bucket lifecycle expiration days do not match expected value."
  }
}
