run "bucket_creation_and_properties" {
  command = apply

  assert {
    # Mock rationale: These assertions validate the *planned* state and configuration
    # against the expected values, not against a live AWS resource.
    # Terraform's test framework performs these checks against the generated plan.
    condition     = module.test_cosmic_dust_collector.bucket_id != null
    error_message = "Bucket ID should not be null."
  }

  assert {
    condition     = contains(module.test_cosmic_dust_collector.bucket_id, "test-dust-collector")
    error_message = "Bucket ID should contain the prefix 'test-dust-collector'."
  }

  assert {
    condition     = aws_s3_bucket_public_access_block.cosmic_dust.block_public_acls == true
    error_message = "Public ACLs should be blocked."
  }

  assert {
    condition     = aws_s3_bucket_public_access_block.cosmic_dust.block_public_policy == true
    error_message = "Public policies should be blocked."
  }

  assert {
    condition     = aws_s3_bucket_versioning.cosmic_dust.versioning_configuration[0].status == "Enabled"
    error_message = "Bucket versioning should be enabled."
  }

  assert {
    condition     = aws_s3_bucket_lifecycle_configuration.cosmic_dust.rule[0].expiration[0].days == 10
    error_message = "Lifecycle expiration days should be 10."
  }

  assert {
    condition     = aws_s3_bucket_lifecycle_configuration.cosmic_dust.rule[0].transition[0].days == 3
    error_message = "Lifecycle transition days to IA should be 3."
  }

  assert {
    condition     = aws_s3_bucket_lifecycle_configuration.cosmic_dust.rule[0].transition[0].storage_class == "GLACIER_IR"
    error_message = "Lifecycle transition storage class should be GLACIER_IR."
  }
}
