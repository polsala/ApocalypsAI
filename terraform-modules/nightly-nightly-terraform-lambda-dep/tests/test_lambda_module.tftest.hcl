// Mock rationale: Uses localstack-compatible resources and mocked archive_file to simulate AWS Lambda deployment without real cloud dependency.
test {
  rules = [
    rule {
      name = "lambda_created"
      assert {
        condition     = aws_lambda_function.this != null
        error_message = "Lambda function was not created"
      }
    },
    rule {
      name = "role_attached"
      assert {
        condition     = length(aws_iam_role_policy_attachment.lambda_basic_exec) > 0
        error_message = "IAM role policy attachment failed"
      }
    }
  ]
}

run "setup_lambda" {
  command = apply

  variables {
    function_name         = "TestFunction"
    handler               = "index.handler"
    runtime               = "nodejs18.x"
    source_dir            = "../example/lambda-src"
    memory_size           = 256
    timeout               = 60
    environment_variables = { TEST_ENV = "true" }
  }
}
