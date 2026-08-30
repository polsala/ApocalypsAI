# Mock rationale: Terraform tests should be deterministic and offline.
# Mocking the AWS provider allows us to validate the module's configuration
# and outputs without requiring actual AWS credentials or deploying real resources.
# This ensures fast, repeatable, and isolated testing.
mock_provider "aws" {
  # No specific configuration needed for basic resource attribute checks
}

run "test_resource_creation_and_outputs" {
  command = "apply"

  assert {
    # Check S3 bucket name output
    condition     = module.test_bottle.s3_bucket_name == "test-apocalypsai-digital-message-bottle"
    error_message = "S3 bucket name output does not match expected value."
  }

  assert {
    # Check DynamoDB table name output
    condition     = module.test_bottle.dynamodb_table_name == "test-apocalypsai-MessageBottleMetadata"
    error_message = "DynamoDB table name output does not match expected value."
  }

  assert {
    # Check S3 bucket versioning is enabled
    condition     = aws_s3_bucket.message_bottle.versioning[0].enabled == true
    error_message = "S3 bucket versioning is not enabled."
  }

  assert {
    # Check DynamoDB billing mode
    condition     = aws_dynamodb_table.message_metadata.billing_mode == "PAY_PER_REQUEST"
    error_message = "DynamoDB table billing mode is not PAY_PER_REQUEST."
  }

  assert {
    # Check S3 bucket ACL
    condition     = aws_s3_bucket.message_bottle.acl == "private"
    error_message = "S3 bucket ACL is not private."
  }
}
