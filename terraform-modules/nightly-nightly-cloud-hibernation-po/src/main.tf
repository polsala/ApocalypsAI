resource "aws_iam_role" "hibernation_lambda_role" {
  name = "${var.name_prefix}-lambda-role"

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
}

resource "aws_iam_policy" "hibernation_lambda_policy" {
  name        = "${var.name_prefix}-lambda-policy"
  description = "IAM policy for Lambda to stop/start EC2 instances"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:${var.region}:*:*"
      },
      {
        Action = [
          "ec2:DescribeInstances",
          "ec2:StopInstances",
          "ec2:StartInstances",
        ]
        Effect   = "Allow"
        Resource = "*" # For simplicity, allows managing any EC2 instance. Refine with resource-level permissions if specific ARNs are known.
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "hibernation_lambda_attach" {
  role       = aws_iam_role.hibernation_lambda_role.name
  policy_arn = aws_iam_policy.hibernation_lambda_policy.arn
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  output_path = "${path.module}/lambda_function.zip"
  source_content {
    content  = file("${path.module}/lambda_handler.py")
    filename = "lambda_handler.py"
  }
}

resource "aws_lambda_function" "hibernation_scheduler_lambda" {
  function_name    = "${var.name_prefix}-scheduler-lambda"
  handler          = "lambda_handler.lambda_handler"
  runtime          = "python3.9"
  role             = aws_iam_role.hibernation_lambda_role.arn
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  timeout          = 60 # seconds

  environment {
    variables = {
      REGION        = var.region
      RESOURCE_TAGS = jsonencode(var.resource_tags)
    }
  }
}

resource "aws_cloudwatch_event_rule" "stop_rule" {
  name                = "${var.name_prefix}-stop-rule"
  description         = "CloudWatch rule to stop EC2 instances"
  schedule_expression = var.stop_cron_schedule
}

resource "aws_cloudwatch_event_target" "stop_target" {
  rule      = aws_cloudwatch_event_rule.stop_rule.name
  target_id = "StopInstancesLambda"
  arn       = aws_lambda_function.hibernation_scheduler_lambda.arn
  input     = jsonencode({"detail": {"action": "stop"}})
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_stop" {
  statement_id  = "AllowExecutionFromCloudWatchStop"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.hibernation_scheduler_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.stop_rule.arn
}

resource "aws_cloudwatch_event_rule" "start_rule" {
  name                = "${var.name_prefix}-start-rule"
  description         = "CloudWatch rule to start EC2 instances"
  schedule_expression = var.start_cron_schedule
}

resource "aws_cloudwatch_event_target" "start_target" {
  rule      = aws_cloudwatch_event_rule.start_rule.name
  target_id = "StartInstancesLambda"
  arn       = aws_lambda_function.hibernation_scheduler_lambda.arn
  input     = jsonencode({"detail": {"action": "start"}})
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_start" {
  statement_id  = "AllowExecutionFromCloudWatchStart"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.hibernation_scheduler_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.start_rule.arn
}
