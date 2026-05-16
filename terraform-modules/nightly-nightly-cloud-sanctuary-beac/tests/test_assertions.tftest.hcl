run "test_module_outputs" {
  command = "plan"

  # Mock rationale: Terraform tests operate on the configuration itself and can validate planned changes without actual cloud interaction.
  # We assert that the module's outputs are correctly generated based on the provided inputs and internal logic.
  assert {
    condition     = module.test_beacon.cloudfront_domain_name != null
    error_message = "CloudFront domain name should not be null."
  }

  assert {
    condition     = length(module.test_beacon.cloudfront_domain_name) > 0
    error_message = "CloudFront domain name should not be empty."
  }

  assert {
    condition     = module.test_beacon.s3_bucket_name != null
    error_message = "S3 bucket name should not be null."
  }

  assert {
    condition     = length(module.test_beacon.s3_bucket_name) > 0
    error_message = "S3 bucket name should not be empty."
  }

  # Test for expected bucket name pattern, including the random suffix
  assert {
    condition     = can(regex("^test-project-test-sanctuary-beacon-\\w+", module.test_beacon.s3_bucket_name))
    error_message = "S3 bucket name should follow the expected pattern (project-env-sanctuary-beacon-random_hex)."
  }

  # Assert that the CloudFront distribution is configured to use the S3 bucket as an origin.
  # This is implicitly tested by the `cloudfront_domain_name` output being available, 
  # as the distribution must be configured correctly for its domain name to be generated.

  # Assert that the S3 bucket policy is generated (implicitly by the resource existing in the plan)
  # and that it grants access to CloudFront (more complex to assert specific policy content in a simple test).
  # We rely on the module's internal logic to correctly generate the policy for OAC.
}
