terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# Random pet for chaos resource naming
resource "random_pet" "chaos_garden" {
  length    = 3
  separator = "-"
}

# Create a chaotic S3 bucket
resource "aws_s3_bucket" "chaos_bucket" {
  bucket = "${var.garden_name}-chaos-bucket-${random_pet.chaos_garden.id}"
  acl    = "private"

  tags = {
    Name        = "${var.garden_name}-chaos-bucket"
    Environment = "chaos"
    ChaosLevel  = var.chaos_level
  }
}

# Create a chaotic Lambda function
resource "aws_lambda_function" "chaos_lambda" {
  filename         = data.archive_file.chaos_lambda_zip.output_path
  function_name    = "${var.garden_name}-chaos-lambda-${random_pet.chaos_garden.id}"
  role             = aws_iam_role.lambda_exec.arn
  handler          = "index.handler"
  source_code_hash = filebase64sha256(data.archive_file.chaos_lambda_zip.output_path)
  runtime          = "nodejs20.x"

  environment {
    variables = {
      CHAOS_LEVEL = var.chaos_level
      GARDEN_NAME = var.garden_name
    }
  }

  tags = {
    Name        = "${var.garden_name}-chaos-lambda"
    Environment = "chaos"
  }
}

# Lambda function code
resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.chaos_lambda.function_name
  principal     = "events.amazonaws.com"
}

# CloudWatch Event Rule for chaos scheduling
resource "aws_cloudwatch_event_rule" "chaos_schedule" {
  count  = var.enable_chaos ? 1 : 0
  name   = "${var.garden_name}-chaos-schedule"
  schedule_expression = "rate(5 minutes)"

  tags = {
    Name        = "${var.garden_name}-chaos-schedule"
    Environment = "chaos"
  }
}

resource "aws_cloudwatch_event_target" "chaos_target" {
  count  = var.enable_chaos ? 1 : 0
  rule      = aws_cloudwatch_event_rule.chaos_schedule[0].name
  target_id = "ChaosLambdaTarget"
  arn       = aws_lambda_function.chaos_lambda.arn
}

# IAM role for Lambda execution
resource "aws_iam_role" "lambda_exec" {
  name = "${var.garden_name}-lambda-exec-${random_pet.chaos_garden.id}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Lambda function code archive
data "archive_file" "chaos_lambda_zip" {
  type        = "zip"
  output_path = "${path.module}/chaos_lambda.zip"
  source {
    content = <<-EOT
      exports.handler = async (event) => {
        const AWS = require('aws-sdk');
        const s3 = new AWS.S3();
        
        console.log('Chaos Lambda executing with level:', process.env.CHAOS_LEVEL);
        
        // Random chaos action based on chaos level
        const chaosActions = [
          'log_status',
          'list_buckets',
          'create_object',
          'delete_object',
          'chaos_report'
        ];
        
        const randomAction = chaosActions[Math.floor(Math.random() * chaosActions.length)];
        
        try {
          switch(randomAction) {
            case 'log_status':
              console.log('Chaos Garden Status: All systems nominal (for now)');
              break;
            case 'list_buckets':
              const buckets = await s3.listBuckets().promise();
              console.log('Found buckets:', buckets.Buckets.length);
              break;
            case 'create_object':
              await s3.putObject({
                Bucket: process.env.CHAOS_BUCKET || 'chaos-bucket',
                Key: `chaos-object-${Date.now()}.txt`,
                Body: 'This is a chaotic object'
              }).promise();
              console.log('Created chaotic object');
              break;
            case 'delete_object':
              if (Math.random() < 0.3) { // 30% chance
                const objects = await s3.listObjectsV2({
                  Bucket: process.env.CHAOS_BUCKET || 'chaos-bucket',
                  MaxKeys: 1
                }).promise();
                
                if (objects.Contents && objects.Contents.length > 0) {
                  await s3.deleteObject({
                    Bucket: process.env.CHAOS_BUCKET || 'chaos-bucket',
                    Key: objects.Contents[0].Key
                  }).promise();
                  console.log('Deleted a chaotic object');
                }
              }
              break;
            case 'chaos_report':
              console.log('Chaos Report: Garden is thriving with chaos!');
              break;
          }
        } catch (error) {
          console.error('Chaos error (expected):', error.message);
        }
        
        return {
          statusCode: 200,
          body: JSON.stringify({
            message: 'Chaos executed successfully',
            action: randomAction,
            chaosLevel: process.env.CHAOS_LEVEL
          })
        };
      };
    EOT
    filename = "index.js"
  }
}

# Output the chaos garden information
output "garden_url" {
  description = "URL to monitor your chaos garden"
  value       = "https://console.aws.amazon.com/lambda/home?region=${var.region}#/functions/${aws_lambda_function.chaos_lambda.function_name}"
}

output "chaos_resources" {
  description = "List of created chaos resources"
  value = {
    bucket = aws_s3_bucket.chaos_bucket.id
    lambda = aws_lambda_function.chaos_lambda.arn
    schedule = var.enable_chaos ? aws_cloudwatch_event_rule.chaos_schedule[0].arn : "disabled"
  }
}

output "chaos_schedule" {
  description = "Cron schedule for chaos events"
  value       = var.enable_chaos ? aws_cloudwatch_event_rule.chaos_schedule[0].schedule_expression : "chaos_disabled"
}
