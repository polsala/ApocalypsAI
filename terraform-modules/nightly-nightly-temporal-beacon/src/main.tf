provider "aws" {
  region = var.aws_region
}

resource "aws_cloudwatch_log_group" "beacon_log_group" {
  name              = "/aws/lambda/${var.beacon_name}-function"
  retention_in_days = 7

  tags = {
    Project     = "ApocalypsAI"
    Utility     = "TemporalBeacon"
    ManagedBy   = "Terraform"
  }
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "${var.beacon_name}-lambda-exec-role"

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
    Project     = "ApocalypsAI"
    Utility     = "TemporalBeacon"
    ManagedBy   = "Terraform"
  }
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda/beacon.py"
  output_path = "${path.module}/lambda/beacon.zip"
}

resource "aws_lambda_function" "temporal_beacon" {
  function_name    = "${var.beacon_name}-function"
  handler          = "beacon.handler"
  runtime          = "python3.9"
  role             = aws_iam_role.lambda_exec_role.arn
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  timeout          = 30

  environment {
    variables = {
      BEACON_MESSAGE = var.beacon_message
    }
  }

  tags = {
    Project     = "ApocalypsAI"
    Utility     = "TemporalBeacon"
    ManagedBy   = "Terraform"
  }
}

resource "aws_cloudwatch_event_rule" "beacon_schedule" {
  name                = "${var.beacon_name}-schedule"
  schedule_expression = var.schedule_expression

  tags = {
    Project     = "ApocalypsAI"
    Utility     = "TemporalBeacon"
    ManagedBy   = "Terraform"
  }
}

resource "aws_cloudwatch_event_target" "beacon_target" {
  rule      = aws_cloudwatch_event_rule.beacon_schedule.name
  target_id = "${var.beacon_name}-lambda-target"
  arn       = aws_lambda_function.temporal_beacon.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.temporal_beacon.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.beacon_schedule.arn
}
