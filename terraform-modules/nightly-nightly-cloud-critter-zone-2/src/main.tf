resource "aws_s3_bucket" "critter_food_bowl" {
  bucket = "${var.project_name}-${var.environment}-${var.critter_name}-food-bowl"

  tags = {
    Project     = var.project_name
    Environment = var.environment
    Critter     = var.critter_name
    ManagedBy   = "ApocalypsAI"
  }
}

resource "aws_s3_bucket_public_access_block" "critter_food_bowl_block" {
  bucket = aws_s3_bucket.critter_food_bowl.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_sns_topic" "critter_water_dish" {
  name = "${var.project_name}-${var.environment}-${var.critter_name}-water-dish"

  tags = {
    Project     = var.project_name
    Environment = var.environment
    Critter     = var.critter_name
    ManagedBy   = "ApocalypsAI"
  }
}

data "archive_file" "lullaby_lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda/lullaby.py"
  output_path = "${path.module}/lambda/lullaby.zip"
}

resource "aws_iam_role" "lullaby_lambda_role" {
  name = "${var.project_name}-${var.environment}-${var.critter_name}-lullaby-lambda-role"

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

  tags = {
    Project     = var.project_name
    Environment = var.environment
    Critter     = var.critter_name
    ManagedBy   = "ApocalypsAI"
  }
}

resource "aws_iam_role_policy_attachment" "lullaby_lambda_policy" {
  role       = aws_iam_role.lullaby_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "critter_lullaby_lambda" {
  function_name    = "${var.project_name}-${var.environment}-${var.critter_name}-lullaby"
  handler          = "lullaby.handler"
  runtime          = "python3.9"
  role             = aws_iam_role.lullaby_lambda_role.arn
  filename         = data.archive_file.lullaby_lambda_zip.output_path
  source_code_hash = data.archive_file.lullaby_lambda_zip.output_base64sha256
  timeout          = 30

  tags = {
    Project     = var.project_name
    Environment = var.environment
    Critter     = var.critter_name
    ManagedBy   = "ApocalypsAI"
  }
}

resource "aws_cloudwatch_event_rule" "critter_bedtime_scheduler" {
  name                = "${var.project_name}-${var.environment}-${var.critter_name}-bedtime-scheduler"
  description         = "Triggers the critter lullaby lambda daily at 2 AM UTC"
  schedule_expression = "cron(0 2 * * ? *)" # Every day at 2 AM UTC

  tags = {
    Project     = var.project_name
    Environment = var.environment
    Critter     = var.critter_name
    ManagedBy   = "ApocalypsAI"
  }
}

resource "aws_cloudwatch_event_target" "critter_lullaby_target" {
  rule      = aws_cloudwatch_event_rule.critter_bedtime_scheduler.name
  target_id = "critter-lullaby-lambda"
  arn       = aws_lambda_function.critter_lullaby_lambda.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_lullaby_lambda" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.critter_lullaby_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.critter_bedtime_scheduler.arn
}
