# tests/test_beacon.tftest.hcl
# This file defines tests for the 'nightly-whispering-cloud-beacon' Terraform module.

# Test that the API endpoint output is correctly generated and formatted.
run "test_api_endpoint_output" {
  command = plan

  # Mock rationale: Prevent actual AWS resource creation during testing.
  # We are testing the Terraform configuration and outputs, not the live deployment.
  # This ensures tests are deterministic and offline.
  mock_provider "aws" {
    plan_is_empty = true
    # Mock data for aws_caller_identity to ensure bucket name can be formed
    data "aws_caller_identity" "current" {
      account_id = "123456789012"
    }
  }

  assert {
    condition     = module.beacon_test.api_endpoint != null
    error_message = "API endpoint should be present in outputs."
  }
  assert {
    condition     = can(regex("^https://.*\\.execute-api\\..*\\.amazonaws\\.com/\\$default/whisper$", module.beacon_test.api_endpoint))
    error_message = "API endpoint should be a valid AWS API Gateway URL ending with /whisper."
  }
}

# Test that the core AWS resources (Lambda, API Gateway, Log Group) are configured as expected.
run "test_core_resources_configuration" {
  command = plan

  # Mock rationale: Prevent actual AWS resource creation during testing.
  # We are testing the Terraform configuration, not the live deployment.
  # This ensures tests are deterministic and offline.
  mock_provider "aws" {
    plan_is_empty = true
    # Mock data for aws_caller_identity to ensure bucket name can be formed
    data "aws_caller_identity" "current" {
      account_id = "123456789012"
    }
  }

  # Assertions on aws_lambda_function
  assert {
    condition     = aws_lambda_function.beacon_lambda.function_name == "test-beacon-whisper-collector"
    error_message = "Lambda function name should be 'test-beacon-whisper-collector'."
  }
  assert {
    condition     = aws_lambda_function.beacon_lambda.runtime == "python3.9"
    error_message = "Lambda runtime should be 'python3.9'."
  }
  assert {
    condition     = aws_lambda_function.beacon_lambda.memory_size == 128
    error_message = "Lambda memory size should be 128MB."
  }
  assert {
    condition     = aws_lambda_function.beacon_lambda.timeout == 30
    error_message = "Lambda timeout should be 30 seconds."
  }
  assert {
    condition     = aws_lambda_function.beacon_lambda.handler == "main.handler"
    error_message = "Lambda handler should be 'main.handler'."
  }

  # Assertions on aws_api_gateway_v2_api
  assert {
    condition     = aws_api_gateway_v2_api.beacon_api.name == "test-beacon-whisper-api"
    error_message = "API Gateway name should be 'test-beacon-whisper-api'."
  }
  assert {
    condition     = aws_api_gateway_v2_api.beacon_api.protocol_type == "HTTP"
    error_message = "API Gateway protocol type should be 'HTTP'."
  }

  # Assertions on aws_cloudwatch_log_group
  assert {
    condition     = aws_cloudwatch_log_group.beacon_log_group.name == "/aws/lambda/test-beacon-whisper-collector"
    error_message = "CloudWatch Log Group name should be '/aws/lambda/test-beacon-whisper-collector'."
  }
  assert {
    condition     = aws_cloudwatch_log_group.beacon_log_group.retention_in_days == 7
    error_message = "CloudWatch Log Group retention should be 7 days."
  }

  # Assertions on aws_iam_role
  assert {
    condition     = aws_iam_role.lambda_exec_role.name == "test-beacon-whisper-lambda-exec-role"
    error_message = "IAM role name should be 'test-beacon-whisper-lambda-exec-role'."
  }

  # Assertions on aws_s3_bucket
  assert {
    condition     = aws_s3_bucket.lambda_bucket.bucket == "test-beacon-whisper-lambda-code-123456789012"
    error_message = "S3 bucket name should be 'test-beacon-whisper-lambda-code-123456789012'."
  }
}
