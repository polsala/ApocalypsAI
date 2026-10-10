resource "aws_s3_bucket" "lambda_bucket" {
  bucket = "${var.prefix}-whisper-lambda-code-${data.aws_caller_identity.current.account_id}"
  acl    = "private"

  tags = {
    Name        = "${var.prefix}-whisper-lambda-code"
    Environment = "ApocalypsAI"
  }
}

resource "aws_s3_bucket_public_access_block" "lambda_bucket_block" {
  bucket = aws_s3_bucket.lambda_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda"
  output_path = "${path.module}/lambda.zip"
}

resource "aws_s3_bucket_object" "lambda_code" {
  bucket = aws_s3_bucket.lambda_bucket.id
  key    = "lambda_function.zip"
  source = data.archive_file.lambda_zip.output_path
  etag   = filemd5(data.archive_file.lambda_zip.output_path)
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "${var.prefix}-whisper-lambda-exec-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })

  tags = {
    Name        = "${var.prefix}-whisper-lambda-exec-role"
    Environment = "ApocalypsAI"
  }
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "beacon_lambda" {
  function_name    = "${var.prefix}-whisper-collector"
  handler          = "main.handler"
  runtime          = var.runtime
  memory_size      = var.memory_size
  timeout          = var.timeout
  role             = aws_iam_role.lambda_exec_role.arn
  s3_bucket        = aws_s3_bucket.lambda_bucket.id
  s3_key           = aws_s3_bucket_object.lambda_code.key
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      LOG_LEVEL = "INFO"
    }
  }

  tags = {
    Name        = "${var.prefix}-whisper-collector"
    Environment = "ApocalypsAI"
  }
}

resource "aws_cloudwatch_log_group" "beacon_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.beacon_lambda.function_name}"
  retention_in_days = 7 # Whimsical logs don't need to live forever

  tags = {
    Name        = "${var.prefix}-whisper-log-group"
    Environment = "ApocalypsAI"
  }
}

resource "aws_api_gateway_v2_api" "beacon_api" {
  name          = "${var.prefix}-whisper-api"
  protocol_type = "HTTP"

  tags = {
    Name        = "${var.prefix}-whisper-api"
    Environment = "ApocalypsAI"
  }
}

resource "aws_api_gateway_v2_integration" "beacon_lambda_integration" {
  api_id             = aws_api_gateway_v2_api.beacon_api.id
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
  integration_uri    = aws_lambda_function.beacon_lambda.invoke_arn
}

resource "aws_api_gateway_v2_route" "beacon_route" {
  api_id    = aws_api_gateway_v2_api.beacon_api.id
  route_key = "POST /whisper"
  target    = "integrations/${aws_api_gateway_v2_integration.beacon_lambda_integration.id}"
}

resource "aws_api_gateway_v2_stage" "beacon_stage" {
  api_id      = aws_api_gateway_v2_api.beacon_api.id
  name        = "$default"
  auto_deploy = true

  tags = {
    Name        = "${var.prefix}-whisper-api-stage"
    Environment = "ApocalypsAI"
  }
}

resource "aws_lambda_permission" "api_gateway_permission" {
  statement_id  = "AllowAPIGatewayInvokeLambda"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.beacon_lambda.function_name
  principal     = "apigateway.amazonaws.com"

  # The /*/* portion allows invocation from any stage, any method, any path
  source_arn = "${aws_api_gateway_v2_api.beacon_api.execution_arn}/*/*"
}

data "aws_caller_identity" "current" {}
