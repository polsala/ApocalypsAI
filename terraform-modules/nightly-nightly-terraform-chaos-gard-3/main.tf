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
  region = var.aws_region
}

variable "garden_name" {
  description = "Name prefix for all resources"
  type        = string
  default     = "chaos-garden"
}

variable "chaos_factor" {
  description = "Probability (0.0-1.0) of resource destruction"
  type        = number
  default     = 0.2
}

variable "s3_buckets" {
  description = "List of S3 bucket names to create"
  type        = list(string)
  default     = ["flowers", "trees", "bushes"]
}

variable "dynamodb_tables" {
  description = "List of DynamoDB table names to create"
  type        = list(string)
  default     = ["insects", "birds", "soil"]
}

variable "lambda_functions" {
  description = "List of Lambda function names to create"
  type        = list(string)
  default     = ["watering", "pruning", "harvesting"]
}

variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

# Create S3 buckets
resource "aws_s3_bucket" "garden_buckets" {
  for_each = toset(var.s3_buckets)
  
  bucket = "${var.garden_name}-${each.key}-${random_pet.bucket_suffix[each.key].id}"
  acl    = "private"
  
  tags = {
    Name        = "${var.garden_name}-${each.key}"
    Environment = "chaos-garden"
    CreatedBy   = "terraform"
  }
}

resource "random_pet" "bucket_suffix" {
  for_each = toset(var.s3_buckets)
}

# Create DynamoDB tables
resource "aws_dynamodb_table" "garden_tables" {
  for_each = toset(var.dynamodb_tables)
  
  name         = "${var.garden_name}-${each.key}-${random_pet.table_suffix[each.key].id}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"
  
  attribute {
    name = "id"
    type = "S"
  }
  
  tags = {
    Name        = "${var.garden_name}-${each.key}"
    Environment = "chaos-garden"
    CreatedBy   = "terraform"
  }
}

resource "random_pet" "table_suffix" {
  for_each = toset(var.dynamodb_tables)
}

# Create Lambda functions
resource "aws_lambda_function" "garden_functions" {
  for_each = toset(var.lambda_functions)
  
  function_name = "${var.garden_name}-${each.key}-${random_pet.function_suffix[each.key].id}"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "index.handler"
  runtime       = "python3.9"
  
  filename         = "${path.module}/lambda/${each.key}.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda/${each.key}.zip")
  
  tags = {
    Name        = "${var.garden_name}-${each.key}"
    Environment = "chaos-garden"
    CreatedBy   = "terraform"
  }
}

resource "random_pet" "function_suffix" {
  for_each = toset(var.lambda_functions)
}

# IAM role for Lambda execution
resource "aws_iam_role" "lambda_exec" {
  name = "${var.garden_name}-lambda-exec-${random_pet.role_suffix.id}"
  
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

resource "random_pet" "role_suffix" {}

# Chaos destruction mechanism
resource "null_resource" "chaos_destruction" {
  count = length(var.s3_buckets) + length(var.dynamodb_tables) + length(var.lambda_functions)
  
  triggers = {
    random_seed = random_integer.chaos_seed.result
  }
  
  provisioner "local-exec" {
    when    = destroy
    command = "echo 'Chaos strikes! Resource ${count.index} has been destroyed.'"
  }
}

resource "random_integer" "chaos_seed" {
  min = 0
  max = 100
}

# Output the garden health
output "garden_health" {
  value = "${var.garden_name} is ${100 - (var.chaos_factor * 100)}% healthy"
}

output "surviving_resources" {
  value = [
    for bucket in aws_s3_bucket.garden_buckets : bucket.id
    if random_integer.chaos_seed.result > (var.chaos_factor * 100)
  ]
}

output "destroyed_resources" {
  value = [
    for bucket in aws_s3_bucket.garden_buckets : bucket.id
    if random_integer.chaos_seed.result <= (var.chaos_factor * 100)
  ]
}

# Create a CloudWatch dashboard for monitoring
resource "aws_cloudwatch_dashboard" "garden_dashboard" {
  dashboard_name = "${var.garden_name}-dashboard"
  
  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 12
        height = 6
        properties = {
          metrics = [
            ["AWS/S3", "BucketSizeBytes", "BucketName", "${aws_s3_bucket.garden_buckets[0].id}"]
          ]
          period = 300
          stat   = "Average"
          region = var.aws_region
          title  = "Garden Health Metrics"
        }
      }
    ]
  })
}
