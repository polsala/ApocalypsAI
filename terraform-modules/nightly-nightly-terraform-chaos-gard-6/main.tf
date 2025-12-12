terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Random provider for chaos scenarios
provider "random" {}

# Generate random chaos garden ID
resource "random_pet" "chaos_garden_id" {
  length = 3
}

# Create VPC for chaos garden
resource "aws_vpc" "chaos_garden" {
  cidr_block = var.vpc_cidr_block
  tags = {
    Name        = "${var.environment}-chaos-garden-vpc"
    Environment = var.environment
    ChaosGarden = random_pet.chaos_garden_id.id
  }
}

# Create Internet Gateway
resource "aws_internet_gateway" "chaos_garden" {
  vpc_id = aws_vpc.chaos_garden.id
  tags = {
    Name        = "${var.environment}-chaos-garden-igw"
    Environment = var.environment
    ChaosGarden = random_pet.chaos_garden_id.id
  }
}

# Create public subnet
resource "aws_subnet" "chaos_garden_public" {
  vpc_id                  = aws_vpc.chaos_garden.id
  cidr_block              = cidrsubnet(var.vpc_cidr_block, 8, 1)
  map_public_ip_on_launch = true
  tags = {
    Name        = "${var.environment}-chaos-garden-public-subnet"
    Environment = var.environment
    ChaosGarden = random_pet.chaos_garden_id.id
  }
}

# Create route table
resource "aws_route_table" "chaos_garden_public" {
  vpc_id = aws_vpc.chaos_garden.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.chaos_garden.id
  }
  tags = {
    Name        = "${var.environment}-chaos-garden-public-rt"
    Environment = var.environment
    ChaosGarden = random_pet.chaos_garden_id.id
  }
}

# Associate route table with subnet
resource "aws_route_table_association" "chaos_garden_public" {
  subnet_id      = aws_subnet.chaos_garden_public.id
  route_table_id = aws_route_table.chaos_garden_public.id
}

# Create security group for chaos garden
resource "aws_security_group" "chaos_garden" {
  name        = "${var.environment}-chaos-garden-sg"
  description = "Security group for chaos garden resources"
  vpc_id      = aws_vpc.chaos_garden.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "SSH access"
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP access"
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS access"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name        = "${var.environment}-chaos-garden-sg"
    Environment = var.environment
    ChaosGarden = random_pet.chaos_garden_id.id
  }
}

# Create S3 buckets for chaos garden
resource "aws_s3_bucket" "chaos_garden" {
  count = var.create_s3_buckets ? var.s3_bucket_count : 0

  bucket = "${var.environment}-chaos-garden-bucket-${count.index + 1}-${random_pet.chaos_garden_id.id}"
  acl    = "private"

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    Name        = "${var.environment}-chaos-garden-bucket-${count.index + 1}"
    Environment = var.environment
    ChaosGarden = random_pet.chaos_garden_id.id
  }
}

# Create S3 bucket objects for chaos (data exhaustion)
resource "aws_s3_object" "chaos_data" {
  count = var.enable_resource_exhaustion && var.create_s3_buckets ? var.s3_bucket_count * 5 : 0

  bucket = aws_s3_bucket.chaos_garden[count.index % var.s3_bucket_count].id
  key    = "chaos-data-${count.index}.txt"
  content = "Chaos data for testing resource exhaustion scenarios. This file contains random data to fill up the S3 bucket. "
  content_type = "text/plain"
}

# Create EC2 instances for chaos garden
resource "aws_instance" "chaos_garden" {
  count = var.create_ec2_instances ? var.ec2_instance_count : 0

  ami           = data.aws_ami.ubuntu.id
  instance_type = var.ec2_instance_type

  subnet_id              = aws_subnet.chaos_garden_public.id
  vpc_security_group_ids = [aws_security_group.chaos_garden.id]

  user_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get install -y stress
              EOF

  tags = {
    Name        = "${var.environment}-chaos-garden-ec2-${count.index + 1}"
    Environment = var.environment
    ChaosGarden = random_pet.chaos_garden_id.id
  }
}

# Create RDS instances for chaos garden
resource "aws_db_instance" "chaos_garden" {
  count = var.create_rds_instances ? 1 : 0

  identifier = "${var.environment}-chaos-garden-rds-${random_pet.chaos_garden_id.id}"

  engine         = "mysql"
  engine_version = "8.0"
  instance_class = var.rds_instance_class
  allocated_storage = 20

  username = "admin"
  password = "ChaosGarden123!"
  db_name  = "chaosdb"

  vpc_security_group_ids = [aws_security_group.chaos_garden.id]
  db_subnet_group_name   = aws_db_subnet_group.chaos_garden.name

  skip_final_snapshot = true
  publicly_accessible = true

  tags = {
    Name        = "${var.environment}-chaos-garden-rds"
    Environment = var.environment
    ChaosGarden = random_pet.chaos_garden_id.id
  }
}

# Create DB subnet group
resource "aws_db_subnet_group" "chaos_garden" {
  name       = "${var.environment}-chaos-garden-db-subnet-group"
  subnet_ids = [aws_subnet.chaos_garden_public.id]

  tags = {
    Name        = "${var.environment}-chaos-garden-db-subnet-group"
    Environment = var.environment
    ChaosGarden = random_pet.chaos_garden_id.id
  }
}

# Create Lambda functions for chaos garden
resource "aws_lambda_function" "chaos_garden" {
  count = var.create_lambda_functions ? var.lambda_function_count : 0

  filename         = "lambda_function.zip"
  function_name    = "${var.environment}-chaos-garden-lambda-${count.index + 1}"
  role             = aws_iam_role.lambda_exec.arn
  handler          = "index.handler"
  source_code_hash = filebase64sha256("lambda_function.zip")
  runtime          = "python3.9"

  environment {
    variables = {
      CHAOS_LEVEL = var.chaos_level
    }
  }

  tags = {
    Name        = "${var.environment}-chaos-garden-lambda-${count.index + 1}"
    Environment = var.environment
    ChaosGarden = random_pet.chaos_garden_id.id
  }
}

# Create IAM role for Lambda execution
resource "aws_iam_role" "lambda_exec" {
  name = "${var.environment}-chaos-garden-lambda-role"

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

# Create IAM policy for Lambda
resource "aws_iam_policy" "lambda_policy" {
  name        = "${var.environment}-chaos-garden-lambda-policy"
  description = "Policy for Lambda functions in chaos garden"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# Attach policy to role
resource "aws_iam_role_policy_attachment" "lambda_policy_attach" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

# Create CloudWatch log groups for Lambda
resource "aws_cloudwatch_log_group" "lambda_logs" {
  count = var.create_lambda_functions ? var.lambda_function_count : 0

  name              = "/aws/lambda/${var.environment}-chaos-garden-lambda-${count.index + 1}"
  retention_in_days = 7

  tags = {
    Name        = "${var.environment}-chaos-garden-lambda-logs-${count.index + 1}"
    Environment = var.environment
    ChaosGarden = random_pet.chaos_garden_id.id
  }
}

# Create CloudWatch dashboard for chaos garden monitoring
resource "aws_cloudwatch_dashboard" "chaos_garden" {
  dashboard_name = "${var.environment}-chaos-garden-dashboard"

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
            ["AWS/EC2", "CPUUtilization", "InstanceId", "${aws_instance.chaos_garden[0].id}"]
          ]
          period = 300
          stat   = "Average"
          region = var.aws_region
          title  = "EC2 CPU Utilization"
        }
      },
      {
        type   = "metric"
        x      = 12
        y      = 0
        width  = 12
        height = 6
        properties = {
          metrics = [
            ["AWS/RDS", "CPUUtilization", "DBInstanceIdentifier", "${aws_db_instance.chaos_garden[0].id}"]
          ]
          period = 300
          stat   = "Average"
          region = var.aws_region
          title  = "RDS CPU Utilization"
        }
      }
    ]
  })

  tags = {
    Name        = "${var.environment}-chaos-garden-dashboard"
    Environment = var.environment
    ChaosGarden = random_pet.chaos_garden_id.id
  }
}

# Create CloudWatch alarms for chaos scenarios
resource "aws_cloudwatch_metric_alarm" "chaos_ec2_cpu_high" {
  count = var.create_ec2_instances ? var.ec2_instance_count : 0

  alarm_name          = "${var.environment}-chaos-garden-ec2-cpu-high-${count.index + 1}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "120"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors ec2 cpu utilization"
  alarm_actions       = var.enable_random_failures ? [aws_sns_topic.chaos_notifications.arn] : []

  dimensions = {
    InstanceId = aws_instance.chaos_garden[count.index].id
  }

  tags = {
    Name        = "${var.environment}-chaos-garden-ec2-cpu-alarm-${count.index + 1}"
    Environment = var.environment
    ChaosGarden = random_pet.chaos_garden_id.id
  }
}

# Create SNS topic for chaos notifications
resource "aws_sns_topic" "chaos_notifications" {
  name = "${var.environment}-chaos-garden-notifications"

  tags = {
    Name        = "${var.environment}-chaos-garden-sns"
    Environment = var.environment
    ChaosGarden = random_pet.chaos_garden_id.id
  }
}

# Create random resources for chaos scenarios
resource "random_integer" "chaos_trigger" {
  count = var.create_ec2_instances ? var.ec2_instance_count : 0
  min   = 1
  max   = 100
}

# Create chaos scenarios based on chaos level
resource "aws_cloudwatch_event_rule" "chaos_scenario" {
  count = var.chaos_level == "high" ? 3 : var.chaos_level == "medium" ? 2 : 1

  name        = "${var.environment}-chaos-scenario-${count.index + 1}"
  description = "Chaos scenario ${count.index + 1} for chaos garden"

  schedule_expression = "rate(5 minutes)"

  tags = {
    Name        = "${var.environment}-chaos-scenario-${count.index + 1}"
    Environment = var.environment
    ChaosGarden = random_pet.chaos_garden_id.id
  }
}

resource "aws_cloudwatch_event_target" "chaos_scenario_target" {
  count     = length(aws_cloudwatch_event_rule.chaos_scenario)
  rule      = aws_cloudwatch_event_rule.chaos_scenario[count.index].name
  target_id = "ChaosScenario${count.index + 1}"
  arn       = aws_lambda_function.chaos_garden[0].arn
}

# Data source for Ubuntu AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Outputs
output "chaos_garden_id" {
  description = "Unique identifier for the chaos garden"
  value       = random_pet.chaos_garden_id.id
}

output "ec2_instance_ids" {
  description = "List of created EC2 instance IDs"
  value       = aws_instance.chaos_garden[*].id
}

output "s3_bucket_names" {
  description = "List of created S3 bucket names"
  value       = aws_s3_bucket.chaos_garden[*].id
}

output "rds_instance_ids" {
  description = "List of created RDS instance IDs"
  value       = aws_db_instance.chaos_garden[*].id
}

output "lambda_function_arns" {
  description = "List of created Lambda function ARNs"
  value       = aws_lambda_function.chaos_garden[*].arn
}

output "vpc_id" {
  description = "VPC ID for the chaos garden"
  value       = aws_vpc.chaos_garden.id
}

output "security_group_id" {
  description = "Security group ID for the chaos garden"
  value       = aws_security_group.chaos_garden.id
}

output "cloudwatch_dashboard_url" {
  description = "CloudWatch dashboard URL for monitoring"
  value       = "https://console.aws.amazon.com/cloudwatch/home?region=${var.aws_region}#dashboards:name=${var.environment}-chaos-garden-dashboard"
}
