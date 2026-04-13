// Mock rationale: This test verifies that all expected resources are created correctly when given valid input values.
// It does not connect to real AWS infrastructure due to use of `mock_provider`.

mock_provider "aws" {}

variables {
  function_name = "test-lambda"
  handler       = "index.handler"
  runtime       = "nodejs18.x"
  filename      = "test.zip"
  timeout       = 10
  memory_size   = 256
}

run "plan_lambda_resources" {
  command = plan

  assert {
    condition     = aws_iam_role.lambda_exec.name == "test-lambda-role"
    error_message = "IAM role name mismatch"
  }

  assert {
    condition     = aws_lambda_function.this.function_name == "test-lambda"
    error_message = "Lambda function name mismatch"
  }

  assert {
    condition     = aws_cloudwatch_log_group.lambda_logs.name == "/aws/lambda/test-lambda"
    error_message = "CloudWatch log group name mismatch"
  }
}
