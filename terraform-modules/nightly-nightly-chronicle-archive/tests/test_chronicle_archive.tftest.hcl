# Mock rationale: This test file uses Terraform's native testing framework.
# The 'run "plan"' block performs a dry run without actual provisioning,
# making the test deterministic and offline by inspecting the planned state.
# Assertions check the configuration of resources as they would be created.

run "plan" {
  command = "plan"

  assert {
    condition     = module.test_chronicle_archive.bucket_id == "apocalypsai-test-chronicle-archive-12345"
    error_message = "Bucket ID output does not match expected name."
  }

  assert {
    condition     = module.test_chronicle_archive.bucket_arn == "arn:aws:s3:::apocalypsai-test-chronicle-archive-12345"
    error_message = "Bucket ARN output does not match expected format."
    # Mock rationale: ARN format is predictable based on bucket name,
    # allowing assertion without actual resource creation.
  }

  assert {
    condition     = plan.resource_changes["aws_s3_bucket.chronicle_archive"].change.after.bucket == "apocalypsai-test-chronicle-archive-12345"
    error_message = "Planned S3 bucket name does not match expected."
  }

  assert {
    condition     = plan.resource_changes["aws_s3_bucket_versioning.chronicle_archive_versioning"].change.after.versioning_configuration[0].status == "Enabled"
    error_message = "Planned S3 bucket versioning is not enabled."
  }

  assert {
    condition     = plan.resource_changes["aws_s3_bucket_server_side_encryption_configuration.chronicle_archive_encryption"].change.after.rule[0].apply_server_side_encryption_by_default[0].sse_algorithm == "AES256"
    error_message = "Planned S3 bucket encryption algorithm is not AES256."
  }

  assert {
    condition     = plan.resource_changes["aws_s3_bucket_public_access_block.chronicle_archive_public_access_block"].change.after.block_public_acls == true
    error_message = "Planned S3 bucket public ACL blocking is not enabled."
  }

  assert {
    condition     = plan.resource_changes["aws_s3_bucket_lifecycle_configuration.chronicle_archive_lifecycle[0]"].change.after.rule[0].noncurrent_version_transition[0].days == 30
    error_message = "Planned lifecycle rule noncurrent_version_transition_days does not match."
  }

  assert {
    condition     = plan.resource_changes["aws_s3_bucket_lifecycle_configuration.chronicle_archive_lifecycle[0]"].change.after.rule[0].noncurrent_version_expiration[0].days == 180
    error_message = "Planned lifecycle rule noncurrent_version_expiration_days does not match."
  }
}

run "plan_no_lifecycle" {
  command = "plan"
  variables {
    enable_lifecycle_rules = false
  }

  assert {
    condition     = length(plan.resource_changes["aws_s3_bucket_lifecycle_configuration.chronicle_archive_lifecycle"]) == 0
    error_message = "Lifecycle configuration should not be planned when disabled."
  }
}
