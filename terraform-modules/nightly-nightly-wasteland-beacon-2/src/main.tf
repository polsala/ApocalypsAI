resource "aws_lambda_function" "beacon_lambda" {
  function_name    = "${var.beacon_name}-lambda"
  handler          = "lambda_beacon.handler"
  runtime          = "python3.9"
  timeout          = 30
  memory_size      = 128
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  role             = aws_iam_role.lambda_exec_role.arn

  tags = {
    Name        = "${var.beacon_name}-beacon-lambda"
    Environment = "ApocalypsAI"
    Utility     = "WastelandBeacon"
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
    Name        = "${var.beacon_name}-lambda-exec-role"
    Environment = "ApocalypsAI"
    Utility     = "WastelandBeacon"
  }
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_cloudwatch_log_group" "beacon_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.beacon_lambda.function_name}"
  retention_in_days = 7 # Keep logs for a week

  tags = {
    Name        = "${var.beacon_name}-beacon-log-group"
    Environment = "ApocalypsAI"
    Utility     = "WastelandBeacon"
  }
}

resource "aws_cloudwatch_event_rule" "beacon_schedule" {
  name                = "${var.beacon_name}-schedule"
  description         = "Triggers the Wasteland Beacon Lambda function"
  schedule_expression = var.schedule_expression

  tags = {
    Name        = "${var.beacon_name}-beacon-schedule"
    Environment = "ApocalypsAI"
    Utility     = "WastelandBeacon"
  }
}

resource "aws_cloudwatch_event_target" "beacon_target" {
  rule      = aws_cloudwatch_event_rule.beacon_schedule.name
  target_id = "${var.beacon_name}-lambda-target"
  arn       = aws_lambda_function.beacon_lambda.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.beacon_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.beacon_schedule.arn
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda_beacon.py"
  output_path = "${path.module}/lambda_beacon.zip"
}
