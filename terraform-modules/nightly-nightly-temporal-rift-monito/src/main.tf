resource "aws_s3_bucket" "lambda_code_bucket" {
  bucket = var.s3_bucket_name
  tags = {
    Environment = "ApocalypsAI"
    Utility     = "TemporalRiftMonitor"
  }
}

resource "aws_s3_bucket_acl" "lambda_code_bucket_acl" {
  bucket = aws_s3_bucket.lambda_code_bucket.id
  acl    = "private"
}

resource "aws_s3_object" "lambda_zip" {
  bucket = aws_s3_bucket.lambda_code_bucket.id
  key    = "temporal_rift_monitor_lambda.zip"
  source = data.archive_file.lambda_zip.output_path
  etag   = filemd5(data.archive_file.lambda_zip.output_path)
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda_function.py"
  output_path = "/tmp/temporal_rift_monitor_lambda.zip" # Temporary path for local archive creation
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "${var.prefix}-temporal-rift-monitor-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "temporal_rift_monitor" {
  function_name    = "${var.prefix}-temporal-rift-monitor"
  handler          = "lambda_function.handler"
  runtime          = "python3.9"
  role             = aws_iam_role.lambda_exec_role.arn
  s3_bucket        = aws_s3_bucket.lambda_code_bucket.id
  s3_key           = aws_s3_object.lambda_zip.key
  timeout          = 30
  memory_size      = 128

  environment {
    variables = {
      STABLE_TIME           = var.stable_time
      RIFT_THRESHOLD_SECONDS = var.rift_threshold_seconds
    }
  }

  tags = {
    Environment = "ApocalypsAI"
    Utility     = "TemporalRiftMonitor"
  }
}

resource "aws_cloudwatch_event_rule" "schedule" {
  name                = "${var.prefix}-temporal-rift-monitor-schedule"
  schedule_expression = var.schedule_expression
  description         = "Triggers the Temporal Rift Monitor Lambda function"
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.schedule.name
  target_id = "TemporalRiftMonitorLambda"
  arn       = aws_lambda_function.temporal_rift_monitor.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_invoke_lambda" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.temporal_rift_monitor.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.schedule.arn
}

variable "prefix" {
  description = "A prefix for all resources created by this module."
  type        = string
  default     = "apocalypsai"
}

variable "s3_bucket_name" {
  description = "The name of the S3 bucket to store the Lambda code."
  type        = string
}

variable "schedule_expression" {
  description = "The CloudWatch schedule expression (e.g., 'rate(5 minutes)' or 'cron(0 0 * * ? *)')."
  type        = string
  default     = "rate(15 minutes)"
}

variable "stable_time" {
  description = "The ISO 8601 formatted string representing the 'stable' time for rift detection (e.g., '2000-01-01T00:00:00Z')."
  type        = string
  default     = "2000-01-01T00:00:00Z"
}

variable "rift_threshold_seconds" {
  description = "The time difference in seconds beyond which a 'temporal rift' is detected."
  type        = number
  default     = 3600 # 1 hour
}

output "lambda_function_name" {
  description = "The name of the deployed Lambda function."
  value       = aws_lambda_function.temporal_rift_monitor.function_name
}

output "cloudwatch_event_rule_name" {
  description = "The name of the CloudWatch Event Rule."
  value       = aws_cloudwatch_event_rule.schedule.name
}
