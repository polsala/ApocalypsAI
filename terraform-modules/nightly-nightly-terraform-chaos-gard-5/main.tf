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

# Random pet name for resource naming
resource "random_pet" "garden_name" {
  prefix    = var.garden_name
  separator = "-"
}

# EC2 Instances (Chaos Garden Beds)
resource "aws_instance" "chaos_instances" {
  count = var.create_ec2_instances ? var.ec2_instance_count : 0
  
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  
  tags = {
    Name        = "${random_pet.garden_name.id}-bed-${count.index + 1}"
    Garden      = random_pet.garden_name.id
    ChaosGarden = "true"
    Purpose     = "ChaosExperiment"
  }
  
  lifecycle {
    ignore_changes = [user_data]
  }
}

# Lambda Functions (Chaos Pollinators)
resource "aws_lambda_function" "chaos_pollinators" {
  count = var.create_lambda_functions ? var.lambda_function_count : 0
  
  function_name = "${random_pet.garden_name.id}-pollinator-${count.index + 1}"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "index.handler"
  runtime       = "python3.9"
  
  filename         = "${path.module}/lambda/chaos_pollinator.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda/chaos_pollinator.zip")
  
  environment {
    variables = {
      GARDEN_NAME = random_pet.garden_name.id
      INSTANCE_ID = element(aws_instance.chaos_instances.*.id, count.index)
    }
  }
  
  tags = {
    Garden      = random_pet.garden_name.id
    ChaosGarden = "true"
    Purpose     = "ChaosExperiment"
  }
}

# S3 Buckets (Chaos Watering Cans)
resource "aws_s3_bucket" "chaos_buckets" {
  count = var.create_s3_buckets ? var.s3_bucket_count : 0
  
  bucket = "${random_pet.garden_name.id}-watering-can-${count.index + 1}-${random_id.bucket_suffix.hex}"
  acl    = "private"
  
  tags = {
    Garden      = random_pet.garden_name.id
    ChaosGarden = "true"
    Purpose     = "ChaosExperiment"
  }
}

resource "random_id" "bucket_suffix" {
  count  = var.create_s3_buckets ? var.s3_bucket_count : 0
  byte_length = 4
}

# RDS Instances (Chaos Fertilizer)
resource "aws_db_instance" "chaos_fertilizer" {
  count = var.create_rds_instances ? var.rds_instance_count : 0
  
  identifier = "${random_pet.garden_name.id}-fertilizer-${count.index + 1}"
  
  engine         = "postgres"
  instance_class = "db.t3.micro"
  allocated_storage = 20
  
  username = "chaosadmin"
  password = random_password.db_password.result
  
  skip_final_snapshot = true
  
  tags = {
    Garden      = random_pet.garden_name.id
    ChaosGarden = "true"
    Purpose     = "ChaosExperiment"
  }
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda_exec" {
  name = "${random_pet.garden_name.id}-lambda-exec"
  
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

# CloudWatch Events for Chaos Experiments
resource "aws_cloudwatch_event_rule" "chaos_scheduler" {
  count = var.enable_chaos_experiments ? 1 : 0
  
  name                = "${random_pet.garden_name.id}-chaos-scheduler"
  schedule_expression = var.chaos_schedule
  
  tags = {
    Garden      = random_pet.garden_name.id
    ChaosGarden = "true"
  }
}

resource "aws_cloudwatch_event_target" "chaos_target" {
  count = var.enable_chaos_experiments ? 1 : 0
  
  rule      = aws_cloudwatch_event_rule.chaos_scheduler[0].name
  target_id = "ChaosTarget"
  arn       = aws_lambda_function.chaos_pollinators[0].arn
}

# CloudWatch Events for Cleanup
resource "aws_cloudwatch_event_rule" "cleanup_scheduler" {
  count = var.enable_automatic_cleanup ? 1 : 0
  
  name                = "${random_pet.garden_name.id}-cleanup-scheduler"
  schedule_expression = var.cleanup_schedule
  
  tags = {
    Garden      = random_pet.garden_name.id
    ChaosGarden = "true"
  }
}

resource "aws_cloudwatch_event_target" "cleanup_target" {
  count = var.enable_automatic_cleanup ? 1 : 0
  
  rule      = aws_cloudwatch_event_rule.cleanup_scheduler[0].name
  target_id = "CleanupTarget"
  arn       = aws_lambda_function.cleanup_garden[0].arn
}

# Cleanup Lambda Function
resource "aws_lambda_function" "cleanup_garden" {
  count = var.enable_automatic_cleanup ? 1 : 0
  
  function_name = "${random_pet.garden_name.id}-cleanup-garden"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "index.handler"
  runtime       = "python3.9"
  
  filename         = "${path.module}/lambda/cleanup_garden.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda/cleanup_garden.zip")
  
  environment {
    variables = {
      GARDEN_NAME = random_pet.garden_name.id
    }
  }
  
  tags = {
    Garden      = random_pet.garden_name.id
    ChaosGarden = "true"
    Purpose     = "Cleanup"
  }
}

# CloudWatch Dashboard
resource "aws_cloudwatch_dashboard" "chaos_garden_dashboard" {
  count = var.enable_cloudwatch_dashboard ? 1 : 0
  
  dashboard_name = "${random_pet.garden_name.id}-chaos-dashboard"
  
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
            ["AWS/EC2", "CPUUtilization", "InstanceId", "${element(aws_instance.chaos_instances.*.id, 0)}"],
            ["AWS/Lambda", "Errors", "FunctionName", "${element(aws_lambda_function.chaos_pollinators.*.function_name, 0)}"],
            ["AWS/RDS", "CPUUtilization", "DBInstanceIdentifier", "${element(aws_db_instance.chaos_fertilizer.*.identifier, 0)}"]
          ]
          period = 300
          stat   = "Average"
          region = var.aws_region
          title  = "Chaos Garden Metrics"
        }
      }
    ]
  })
  
  tags = {
    Garden      = random_pet.garden_name.id
    ChaosGarden = "true"
  }
}

# CloudWatch Alarms
resource "aws_cloudwatch_metric_alarm" "chaos_alarms" {
  count = var.enable_alarms ? var.ec2_instance_count : 0
  
  alarm_name          = "${random_pet.garden_name.id}-bed-${count.index + 1}-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "120"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors ec2 cpu utilization"
  alarm_actions       = var.sns_topic_arn != "" ? [var.sns_topic_arn] : []
  
  dimensions = {
    InstanceId = element(aws_instance.chaos_instances.*.id, count.index)
  }
  
  tags = {
    Garden      = random_pet.garden_name.id
    ChaosGarden = "true"
  }
}

# Data Sources
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical
  
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
  
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Random password for RDS
resource "random_password" "db_password" {
  length  = 16
  special = false
}
