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

# Generate whimsical chaos names
locals {
  chaos_adjectives = [
    "chaotic", "anarchic", "whimsical", "unruly", "mischievous",
    "rebellious", "tempestuous", "zany", "wacky", "bizarre",
    "kaleidoscopic", "psychedelic", "labyrinthine", "enigmatic",
    "paradoxical", "whimsy", "cataclysmic", "turbulent"
  ]
  
  chaos_nouns = [
    "rose", "oak", "daisy", "cactus", "bamboo", "tulip",
    "sequoia", "fern", "moss", "ivy", "lotus", "sunflower",
    "lavender", "jasmine", "orchid", "peony", "hydrangea"
  ]
  
  chaos_name = "${element(local.chaos_adjectives, var.seed % length(local.chaos_adjectives))}-${element(local.chaos_nouns, (var.seed + 1) % length(local.chaos_nouns))}"
}

# Chaos VPC
resource "aws_vpc" "chaos_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name           = "${local.chaos_name}-vpc"
    chaos_garden   = "true"
    environment    = var.environment
    chaos_level    = var.chaos_level
    terraform      = "true"
  }
}

# Chaos Internet Gateway
resource "aws_internet_gateway" "chaos_igw" {
  vpc_id = aws_vpc.chaos_vpc.id

  tags = {
    Name         = "${local.chaos_name}-igw"
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos Subnets (with intentional overlapping CIDRs for chaos)
resource "aws_subnet" "chaos_subnets" {
  count = var.enable_network_chaos ? 3 : 2

  vpc_id                  = aws_vpc.chaos_vpc.id
  cidr_block              = count.index == 0 ? "10.0.1.0/24" : count.index == 1 ? "10.0.2.0/24" : "10.0.1.0/24" # Intentional overlap for chaos
  availability_zone       = "${var.region}${element(["a", "b", "c"], count.index)}"
  map_public_ip_on_launch = count.index == 0 ? true : false

  tags = {
    Name         = "${local.chaos_name}-subnet-${count.index}"
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos Route Table
resource "aws_route_table" "chaos_rt" {
  vpc_id = aws_vpc.chaos_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.chaos_igw.id
  }

  tags = {
    Name         = "${local.chaos_name}-route-table"
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos Route Table Association
resource "aws_route_table_association" "chaos_rta" {
  count = length(aws_subnet.chaos_subnets)

  subnet_id      = aws_subnet.chaos_subnets[count.index].id
  route_table_id = aws_route_table.chaos_rt.id
}

# Chaos Security Group (with intentionally permissive rules)
resource "aws_security_group" "chaos_sg" {
  name        = "${local.chaos_name}-chaos-sg"
  description = "Chaos security group with intentionally permissive rules"
  vpc_id      = aws_vpc.chaos_vpc.id

  # Allow all inbound traffic for chaos
  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic for chaos
  egress {
    from_port   = 0
    to_port     = 65535
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name         = "${local.chaos_name}-chaos-sg"
    chaos_garden = "true"
    environment  = var.environment
    chaos_level  = var.chaos_level
  }
}

# Chaos EC2 Instances (with varying chaos levels)
resource "aws_instance" "chaos_instances" {
  count = var.enable_compute_chaos ? var.instance_count : 0

  ami                    = data.aws_ami.ubuntu.id
  instance_type          = element(var.instance_types, count.index % length(var.instance_types))
  subnet_id              = aws_subnet.chaos_subnets[count.index % length(aws_subnet.chaos_subnets)].id
  vpc_security_group_ids = [aws_security_group.chaos_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              echo "Welcome to the Chaos Garden! Instance: ${count.index}" > /var/log/chaos-welcome.log
              # Intentional chaos: create random load
              dd if=/dev/zero of=/tmp/chaos-file bs=1M count=100
              EOF

  tags = {
    Name         = "${local.chaos_name}-chaos-instance-${count.index}"
    chaos_garden = "true"
    environment  = var.environment
    chaos_level  = var.chaos_level
  }
}

# Chaos S3 Buckets (with unusual naming)
resource "aws_s3_bucket" "chaos_buckets" {
  count = var.enable_storage_chaos ? 3 : 0

  bucket = "${local.chaos_name}-chaos-bucket-${count.index}-${random_id.bucket_suffix.hex}"
  acl    = "private"

  tags = {
    Name         = "${local.chaos_name}-chaos-bucket-${count.index}"
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Random ID for unique bucket naming
resource "random_id" "bucket_suffix" {
  count = var.enable_storage_chaos ? 3 : 0
  byte_length = 4
}

# Chaos S3 Bucket Objects (with random content)
resource "aws_s3_object" "chaos_objects" {
  count = var.enable_storage_chaos ? 5 : 0

  bucket = aws_s3_bucket.chaos_buckets[count.index % length(aws_s3_bucket.chaos_buckets)].id
  key    = "chaos-object-${count.index}.txt"
  content = "This is chaos object number ${count.index} in the garden of chaos!"

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos IAM Role (with broad permissions for testing)
resource "aws_iam_role" "chaos_role" {
  name = "${local.chaos_name}-chaos-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos IAM Policy
resource "aws_iam_policy" "chaos_policy" {
  name        = "${local.chaos_name}-chaos-policy"
  description = "Chaos policy with broad permissions for testing"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:*", "ec2:*", "iam:*"]
        Resource = "*"
      }
    ]
  })
}

# Chaos IAM Role Policy Attachment
resource "aws_iam_role_policy_attachment" "chaos_attachment" {
  role       = aws_iam_role.chaos_role.name
  policy_arn = aws_iam_policy.chaos_policy.arn
}

# Chaos IAM Instance Profile
resource "aws_iam_instance_profile" "chaos_profile" {
  name = "${local.chaos_name}-chaos-profile"
  role = aws_iam_role.chaos_role.name
}

# Data source for latest Ubuntu AMI
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

# Chaos CloudWatch Log Group
resource "aws_cloudwatch_log_group" "chaos_logs" {
  name              = "/aws/chaos-garden/${local.chaos_name}"
  retention_in_days = var.destroy_after_hours > 0 ? 1 : 7

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos Lambda Function (for testing serverless chaos)
resource "aws_lambda_function" "chaos_lambda" {
  count = var.enable_compute_chaos ? 1 : 0

  filename         = data.archive_file.chaos_lambda_zip.output_path
  function_name    = "${local.chaos_name}-chaos-lambda"
  role             = aws_iam_role.chaos_role.arn
  handler          = "index.lambda_handler"
  source_code_hash = data.archive_file.chaos_lambda_zip.output_base64sha256
  runtime          = "python3.9"

  environment {
    variables = {
      CHAOS_LEVEL = var.chaos_level
      ENVIRONMENT = var.environment
    }
  }

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Lambda deployment package
data "archive_file" "chaos_lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda"
  output_path = "${path.module}/chaos_lambda.zip"
}

# Chaos Lambda Permission
resource "aws_lambda_permission" "chaos_lambda_permission" {
  count = var.enable_compute_chaos ? 1 : 0

  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.chaos_lambda[0].function_name
  principal     = "apigateway.amazonaws.com"
}

# Chaos RDS Instance (for database chaos testing)
resource "aws_db_instance" "chaos_rds" {
  count = var.enable_compute_chaos && var.chaos_level == "high" ? 1 : 0

  identifier     = "${local.chaos_name}-chaos-rds"
  engine         = "postgres"
  engine_version = "13.7"
  instance_class = "db.t3.micro"
  allocated_storage = 20

  username = "chaos_user"
  password = "chaos_password_123"
  db_name  = "chaosdb"

  vpc_security_group_ids = [aws_security_group.chaos_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.chaos_subnet_group.name

  skip_final_snapshot = true
  deletion_protection = false

  tags = {
    chaos_garden = "true"
    environment  = var.environment
    chaos_level  = var.chaos_level
  }
}

# RDS Subnet Group
resource "aws_db_subnet_group" "chaos_subnet_group" {
  name       = "${local.chaos_name}-chaos-subnet-group"
  subnet_ids = aws_subnet.chaos_subnets[*].id

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos Auto Scaling Group (for scaling chaos)
resource "aws_autoscaling_group" "chaos_asg" {
  count = var.enable_compute_chaos ? 1 : 0

  name                      = "${local.chaos_name}-chaos-asg"
  max_size                  = var.instance_count
  min_size                  = 1
  desired_capacity          = 2
  health_check_grace_period = 300
  health_check_type         = "EC2"
  force_delete              = true

  vpc_zone_identifier = aws_subnet.chaos_subnets[*].id

  launch_template {
    id      = aws_launch_template.chaos_lt.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "${local.chaos_name}-chaos-asg-instance"
    propagate_at_launch = true
  }

  tag {
    key                 = "chaos_garden"
    value               = "true"
    propagate_at_launch = true
  }
}

# Launch Template for ASG
resource "aws_launch_template" "chaos_lt" {
  count = var.enable_compute_chaos ? 1 : 0

  name_prefix   = "${local.chaos_name}-chaos-lt-"
  image_id      = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  iam_instance_profile {
    name = aws_iam_instance_profile.chaos_profile.name
  }

  vpc_security_group_ids = [aws_security_group.chaos_sg.id]

  user_data = base64encode(<<-EOF
              #!/bin/bash
              echo "Welcome to the Chaos Auto Scaling Group!" > /var/log/chaos-asg.log
              EOF
              )

  tag_specifications {
    resource_type = "instance"
    tags = {
      chaos_garden = "true"
      environment  = var.environment
      chaos_level  = var.chaos_level
    }
  }
}

# Chaos CloudWatch Dashboard
resource "aws_cloudwatch_dashboard" "chaos_dashboard" {
  dashboard_name = "${local.chaos_name}-chaos-dashboard"

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
            ["AWS/EC2", "CPUUtilization", "InstanceId", "${aws_instance.chaos_instances[0].id}"]
          ]
          period = 300
          stat   = "Average"
          region = var.region
          title  = "Chaos Instance CPU"
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
            ["AWS/S3", "BucketSizeBytes", "BucketName", "${aws_s3_bucket.chaos_buckets[0].id}", "StorageType", "StandardStorage"]
          ]
          period = 86400
          stat   = "Average"
          region = var.region
          title  = "Chaos Bucket Size"
        }
      }
    ]
  })

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos SNS Topic (for chaos notifications)
resource "aws_sns_topic" "chaos_notifications" {
  name = "${local.chaos_name}-chaos-notifications"

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos SNS Subscription
resource "aws_sns_topic_subscription" "chaos_subscription" {
  topic_arn = aws_sns_topic.chaos_notifications.arn
  protocol  = "email"
  endpoint  = var.notification_email
}

# Chaos EFS File System
resource "aws_efs_file_system" "chaos_efs" {
  count = var.enable_storage_chaos ? 1 : 0

  creation_token = "${local.chaos_name}-chaos-efs"

  tags = {
    Name         = "${local.chaos_name}-chaos-efs"
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos EFS Mount Target
resource "aws_efs_mount_target" "chaos_efs_mt" {
  count = var.enable_storage_chaos ? length(aws_subnet.chaos_subnets) : 0

  file_system_id  = aws_efs_file_system.chaos_efs[0].id
  subnet_id       = aws_subnet.chaos_subnets[count.index].id
  security_groups = [aws_security_group.chaos_sg.id]
}

# Chaos Secrets Manager Secret
resource "aws_secretsmanager_secret" "chaos_secret" {
  name = "${local.chaos_name}-chaos-secret"

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos Secrets Manager Secret Version
resource "aws_secretsmanager_secret_version" "chaos_secret_version" {
  secret_id = aws_secretsmanager_secret.chaos_secret.id
  secret_string = jsonencode({
    chaos_key = "chaos_value_${random_id.bucket_suffix[0].hex}"
    api_key   = "chaos_api_key_12345"
  })
}

# Chaos Parameter Store Parameter
resource "aws_ssm_parameter" "chaos_parameter" {
  name  = "/chaos-garden/${local.chaos_name}/config"
  type  = "SecureString"
  value = "chaos_parameter_value_${random_id.bucket_suffix[0].hex}"

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos ECS Cluster
resource "aws_ecs_cluster" "chaos_cluster" {
  name = "${local.chaos_name}-chaos-cluster"

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos ECS Task Definition
resource "aws_ecs_task_definition" "chaos_task" {
  count = var.enable_compute_chaos ? 1 : 0

  family                   = "${local.chaos_name}-chaos-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"

  execution_role_arn = aws_iam_role.chaos_role.arn
  task_role_arn      = aws_iam_role.chaos_role.arn

  container_definitions = jsonencode([
    {
      name  = "chaos-container"
      image = "nginx:latest"
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
          protocol      = "tcp"
        }
      ]
      essential = true
    }
  ])

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos ECS Service
resource "aws_ecs_service" "chaos_service" {
  count = var.enable_compute_chaos ? 1 : 0

  name            = "${local.chaos_name}-chaos-service"
  cluster         = aws_ecs_cluster.chaos_cluster.id
  task_definition = aws_ecs_task_definition.chaos_task[0].arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = aws_subnet.chaos_subnets[*].id
    security_groups  = [aws_security_group.chaos_sg.id]
    assign_public_ip = true
  }

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos ALB
resource "aws_lb" "chaos_alb" {
  name               = "${local.chaos_name}-chaos-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.chaos_sg.id]
  subnets            = aws_subnet.chaos_subnets[*].id

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos ALB Target Group
resource "aws_lb_target_group" "chaos_tg" {
  name        = "${local.chaos_name}-chaos-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.chaos_vpc.id
  target_type = "ip"

  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    interval            = 30
    path                = "/"
    matcher             = "200"
    port                = "traffic-port"
    protocol            = "HTTP"
  }

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos ALB Listener
resource "aws_lb_listener" "chaos_listener" {
  load_balancer_arn = aws_lb.chaos_alb.arn
  port              = "80"
  protocol            = "HTTP"

  default_action {
    type             = "fixed-response"
    order            = 1
    fixed_response {
      content_type = "text/plain"
      message_body = "Welcome to the Chaos Garden!"
      status_code  = "200"
    }
  }
}

# Chaos ALB Target Group Attachment
resource "aws_lb_target_group_attachment" "chaos_tga" {
  count = var.enable_compute_chaos ? length(aws_instance.chaos_instances) : 0

  target_group_arn = aws_lb_target_group.chaos_tg.arn
  target_id        = aws_instance.chaos_instances[count.index].private_ip
  port             = 80
}

# Chaos DynamoDB Table
resource "aws_dynamodb_table" "chaos_table" {
  count = var.enable_storage_chaos ? 1 : 0

  name     = "${local.chaos_name}-chaos-table"
  hash_key = "chaos_id"
  billing_mode = "PAY_PER_REQUEST"

  attribute {
    name = "chaos_id"
    type = "S"
  }

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos Kinesis Stream
resource "aws_kinesis_stream" "chaos_stream" {
  count = var.enable_compute_chaos ? 1 : 0

  name             = "${local.chaos_name}-chaos-stream"
  shard_count      = 1
  retention_period = 24

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos Step Functions State Machine
resource "aws_sfn_state_machine" "chaos_state_machine" {
  count = var.enable_compute_chaos ? 1 : 0

  name     = "${local.chaos_name}-chaos-state-machine"
  role_arn = aws_iam_role.chaos_role.arn

  definition = jsonencode({
    Comment = "A chaos state machine"
    StartAt = "StartChaos",
    States = {
      StartChaos = {
        Type = "Task",
        Resource = aws_lambda_function.chaos_lambda[0].arn,
        End = true
      }
    }
  })

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos CloudTrail
resource "aws_cloudtrail" "chaos_trail" {
  name                          = "${local.chaos_name}-chaos-trail"
  s3_bucket_name                = aws_s3_bucket.chaos_buckets[0].id
  s3_key_prefix                 = "chaos"
  include_global_service_events = true
  is_multi_region_trail         = true

  event_selector {
    read_write_type = "All"
    include_management_events = true

    data_resource {
      type   = "AWS::S3::Object"
      values = ["${aws_s3_bucket.chaos_buckets[0].arn}/"]
    }
  }

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos Backup Vault
resource "aws_backup_vault" "chaos_backup_vault" {
  count = var.enable_storage_chaos ? 1 : 0

  name = "${local.chaos_name}-chaos-backup-vault"

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos Backup Plan
resource "aws_backup_plan" "chaos_backup_plan" {
  count = var.enable_storage_chaos ? 1 : 0

  name = "${local.chaos_name}-chaos-backup-plan"

  rule {
    rule_name         = "daily-backup"
    target_vault_name = aws_backup_vault.chaos_backup_vault[0].name
    schedule          = "cron(0 2 * * ? *)"
    start_window_minutes = 60
    completion_window_minutes = 120
    lifecycle {
      move_to_cold_storage_after = 30
      delete_after = 365
    }
  }

  advanced_backup_setting {
    backup_options = {
      WindowsVSS = "enabled"
    }
    resource_type = "EC2"
  }

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos Backup Selection
resource "aws_backup_selection" "chaos_backup_selection" {
  count = var.enable_storage_chaos ? 1 : 0

  name         = "${local.chaos_name}-chaos-backup-selection"
  iam_role_arn = aws_iam_role.chaos_role.arn
  plan_id      = aws_backup_plan.chaos_backup_plan[0].id

  selection_tag {
    type  = "STRINGEQUALS"
    key   = "chaos_garden"
    value = "true"
  }
}

# Chaos WAF Web ACL
resource "aws_wafv2_web_acl" "chaos_waf" {
  name  = "${local.chaos_name}-chaos-waf"
  scope = "REGIONAL"

  default_action {
    allow {}
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "${local.chaos_name}-chaos-waf-metric"
    sampled_requests_enabled   = true
  }

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos WAF Web ACL Association
resource "aws_wafv2_web_acl_association" "chaos_waf_association" {
  count = var.enable_compute_chaos ? 1 : 0

  resource_arn = aws_lb.chaos_alb.arn
  web_acl_arn  = aws_wafv2_web_acl.chaos_waf.arn
}

# Chaos API Gateway REST API
resource "aws_api_gateway_rest_api" "chaos_api" {
  count = var.enable_compute_chaos ? 1 : 0

  name        = "${local.chaos_name}-chaos-api"
  description = "Chaos API Gateway"

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos API Gateway Resource
resource "aws_api_gateway_resource" "chaos_api_resource" {
  count      = var.enable_compute_chaos ? 1 : 0
  rest_api_id = aws_api_gateway_rest_api.chaos_api[0].id
  parent_id   = aws_api_gateway_rest_api.chaos_api[0].root_resource_id
  path_part   = "chaos"
}

# Chaos API Gateway Method
resource "aws_api_gateway_method" "chaos_api_method" {
  count         = var.enable_compute_chaos ? 1 : 0
  rest_api_id   = aws_api_gateway_rest_api.chaos_api[0].id
  resource_id   = aws_api_gateway_resource.chaos_api_resource[0].id
  http_method   = "GET"
  authorization = "NONE"
}

# Chaos API Gateway Integration
resource "aws_api_gateway_integration" "chaos_api_integration" {
  count                 = var.enable_compute_chaos ? 1 : 0
  rest_api_id           = aws_api_gateway_rest_api.chaos_api[0].id
  resource_id           = aws_api_gateway_resource.chaos_api_resource[0].id
  http_method           = aws_api_gateway_method.chaos_api_method[0].http_method
  integration_http_method = "POST"
  type                  = "AWS_PROXY"
  uri                   = aws_lambda_function.chaos_lambda[0].arn
}

# Chaos API Gateway Deployment
resource "aws_api_gateway_deployment" "chaos_api_deployment" {
  count       = var.enable_compute_chaos ? 1 : 0
  rest_api_id = aws_api_gateway_rest_api.chaos_api[0].id
  stage_name  = "chaos"

  triggers = {
    re deployment = sha1(jsonencode(aws_api_gateway_integration.chaos_api_integration[0].body))
  }
}

# Chaos API Gateway Stage
resource "aws_api_gateway_stage" "chaos_api_stage" {
  count       = var.enable_compute_chaos ? 1 : 0
  rest_api_id = aws_api_gateway_deployment.chaos_api_deployment[0].rest_api_id
  deployment_id = aws_api_gateway_deployment.chaos_api_deployment[0].id
  stage_name  = aws_api_gateway_deployment.chaos_api_deployment[0].stage_name
}

# Chaos API Gateway Permission
resource "aws_api_gateway_permission" "chaos_api_permission" {
  count         = var.enable_compute_chaos ? 1 : 0
  rest_api_id   = aws_api_gateway_rest_api.chaos_api[0].id
  resource_id   = aws_api_gateway_resource.chaos_api_resource[0].id
  http_method   = aws_api_gateway_method.chaos_api_method[0].http_method
  authorization = "NONE"
  source_arn    = "${aws_api_gateway_rest_api.chaos_api[0].arn}/*/*"
}

# Chaos CodeCommit Repository
resource "aws_codecommit_repository" "chaos_repo" {
  count = var.enable_compute_chaos ? 1 : 0

  repository_name = "${local.chaos_name}-chaos-repo"
  description     = "Chaos CodeCommit repository"

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos CodeBuild Project
resource "aws_codebuild_project" "chaos_build" {
  count = var.enable_compute_chaos ? 1 : 0

  name         = "${local.chaos_name}-chaos-build"
  service_role = aws_iam_role.chaos_role.arn

  artifacts {
    type = "NO_ARTIFACTS"
  }

  environment {
    type                = "LINUX_CONTAINER"
    image               = "aws/codebuild/amazonlinux2-x86_64-standard:3.0"
    compute_type        = "BUILD_GENERAL1_SMALL"
    privileged_mode     = false
  }

  source {
    type      = "CODECOMMIT"
    location  = aws_codecommit_repository.chaos_repo[0].clone_url_http
    buildspec = "version: 0.2\nphases:\n  build:\n    commands:\n      - echo 'Welcome to the Chaos Build!'"
  }

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos CodePipeline
resource "aws_codepipeline" "chaos_pipeline" {
  count = var.enable_compute_chaos ? 1 : 0

  name     = "${local.chaos_name}-chaos-pipeline"
  role_arn = aws_iam_role.chaos_role.arn

  artifact_store {
    location = aws_s3_bucket.chaos_buckets[0].bucket
    type     = "S3"
  }

  stage {
    name = "Source"
    action {
      name             = "Source"
      category         = "Source"
      owner            = "AWS"
      provider         = "CodeCommit"
      version          = "1"
      output_artifacts = ["source_output"]
      configuration = {
        RepositoryName = aws_codecommit_repository.chaos_repo[0].repository_name
        BranchName     = "main"
      }
    }
  }

  stage {
    name = "Build"
    action {
      name            = "Build"
      category        = "Build"
      owner           = "AWS"
      provider        = "CodeBuild"
      input_artifacts = ["source_output"]
      output_artifacts = ["build_output"]
      version         = "1"
      configuration = {
        ProjectName = aws_codebuild_project.chaos_build[0].name
      }
    }
  }

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos EventBridge Rule
resource "aws_cloudwatch_event_rule" "chaos_event_rule" {
  count = var.enable_compute_chaos ? 1 : 0

  name        = "${local.chaos_name}-chaos-event-rule"
  description = "Chaos EventBridge rule"
  schedule_expression = "rate(5 minutes)"

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos EventBridge Target
resource "aws_cloudwatch_event_target" "chaos_event_target" {
  count = var.enable_compute_chaos ? 1 : 0

  rule      = aws_cloudwatch_event_rule.chaos_event_rule[0].name
  target_id = "chaos-target"
  arn       = aws_lambda_function.chaos_lambda[0].arn
}

# Chaos Glue Database
resource "aws_glue_catalog_database" "chaos_glue_db" {
  count = var.enable_storage_chaos ? 1 : 0

  name = "${local.chaos_name}_chaos_glue_db"

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos Glue Table
resource "aws_glue_catalog_table" "chaos_glue_table" {
  count = var.enable_storage_chaos ? 1 : 0

  name          = "chaos_table"
  database_name = aws_glue_catalog_database.chaos_glue_db[0].name

  table_type = "EXTERNAL_TABLE"

  parameters = {
    EXTERNAL = "TRUE"
  }

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.chaos_buckets[0].bucket}/data/"
    input_format  = "org.apache.hadoop.mapred.TextInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"

    ser_de_info {
      name                  = "LambdaFunctionSerDe"
      serialization_library = "org.openx.data.jsonserde.JsonSerDe"
    }

    columns {
      name = "chaos_id"
      type = "string"
    }

    columns {
      name = "chaos_value"
      type = "string"
    }
  }

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos Athena Workgroup
resource "aws_athena_workgroup" "chaos_athena_wg" {
  count = var.enable_storage_chaos ? 1 : 0

  name = "${local.chaos_name}-chaos-athena-wg"

  configuration {
    bytes_scanned_cutoff_per_query = 100000000
    enforce_workgroup_configuration = true
    publish_cloudwatch_metrics_enabled = true
    result_configuration {
      output_location = "s3://${aws_s3_bucket.chaos_buckets[0].bucket}/athena-results/"
    }
  }

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos Redshift Cluster
resource "aws_redshift_cluster" "chaos_redshift" {
  count = var.enable_storage_chaos && var.chaos_level == "high" ? 1 : 0

  cluster_identifier = "${local.chaos_name}-chaos-redshift"
  database_name      = "chaosdb"
  master_username    = "chaos_user"
  master_password    = "chaos_password_123"
  node_type          = "dc2.large"
  cluster_type       = "single-node"

  vpc_security_group_ids = [aws_security_group.chaos_sg.id]
  subnet_group_name      = aws_db_subnet_group.chaos_subnet_group.name

  skip_final_snapshot = true
  publicly_accessible   = false

  tags = {
    chaos_garden = "true"
    environment  = var.environment
    chaos_level  = var.chaos_level
  }
}

# Chaos Redshift Subnet Group
resource "aws_redshift_subnet_group" "chaos_redshift_subnet_group" {
  count = var.enable_storage_chaos && var.chaos_level == "high" ? 1 : 0

  name       = "${local.chaos_name}-chaos-redshift-subnet-group"
  subnet_ids = aws_subnet.chaos_subnets[*].id

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos SQS Queue
resource "aws_sqs_queue" "chaos_queue" {
  count = var.enable_compute_chaos ? 1 : 0

  name                      = "${local.chaos_name}-chaos-queue"
  delay_seconds             = 90
  max_message_size          = 2048
  message_retention_seconds = 86400
  receive_wait_time_seconds = 10

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos SQS Queue Policy
resource "aws_sqs_queue_policy" "chaos_queue_policy" {
  count = var.enable_compute_chaos ? 1 : 0

  queue_url = aws_sqs_queue.chaos_queue[0].id
  policy    = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Principal = "*"
        Action   = "sqs:SendMessage"
        Resource = aws_sqs_queue.chaos_queue[0].arn
        Condition = {
          ArnEquals = {
            "aws:SourceArn" = aws_sns_topic.chaos_notifications.arn
          }
        }
      }
    ]
  })
}

# Chaos CloudFormation Stack
resource "aws_cloudformation_stack" "chaos_cf_stack" {
  count = var.enable_compute_chaos ? 1 : 0

  name = "${local.chaos_name}-chaos-cf-stack"

  template_body = jsonencode({
    AWSTemplateFormatVersion = "2010-09-09"
    Description = "Chaos CloudFormation stack"
    Resources = {
      ChaosBucket = {
        Type = "AWS::S3::Bucket"
        Properties = {
          BucketName = "${local.chaos_name}-chaos-cf-bucket-${random_id.bucket_suffix[0].hex}"
        }
      }
    }
  })

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos CloudFormation StackSet
resource "aws_cloudformation_stack_set" "chaos_cf_stackset" {
  count = var.enable_compute_chaos ? 1 : 0

  name = "${local.chaos_name}-chaos-cf-stackset"

  administration_role_arn = aws_iam_role.chaos_role.arn
  execution_role_name     = aws_iam_role.chaos_role.name

  template_body = jsonencode({
    AWSTemplateFormatVersion = "2010-09-09"
    Description = "Chaos CloudFormation stack set"
    Resources = {
      ChaosBucket = {
        Type = "AWS::S3::Bucket"
        Properties = {
          BucketName = "${local.chaos_name}-chaos-cf-stackset-bucket-${random_id.bucket_suffix[0].hex}"
        }
      }
    }
  })

  tags = {
    chaos_garden = "true"
    environment  = var.environment
  }
}

# Chaos CloudFormation StackSet Instance
resource "aws_cloudformation_stack_set_instance" "chaos_cf_stackset_instance" {
  count = var.enable_compute_chaos ? 1 : 0

  stack_set_name = aws_cloudformation_stack_set.chaos_cf_stackset[0].name
  region         = var.region
  account_id     = data.aws_caller_identity.current.account_id
}

# Data source for current caller identity
data "aws_caller_identity" "current" {}

# Chaos Cleanup (optional auto-destroy)
resource "time_sleep" "chaos_cleanup" {
  count = var.destroy_after_hours > 0 ? 1 : 0

  create_duration = "${var.destroy_after_hours}h"

  triggers = {
    destroy = "${aws_vpc.chaos_vpc.id}"
  }
}

# Null resource for cleanup trigger
resource "null_resource" "chaos_destroy_trigger" {
  count = var.destroy_after_hours > 0 ? 1 : 0

  triggers = {
    cleanup_time = time_sleep.chaos_cleanup[0].id
  }

  provisioner "local-exec" {
    command = "echo 'Chaos Garden cleanup triggered after ${var.destroy_after_hours} hours'"
  }
}

# Lambda function code directory
# lambda/index.py
# (This file should be created in the lambda/ directory)
# Content:
# def lambda_handler(event, context):
#     return {
#         'statusCode': 200,
#         'body': json.dumps('Welcome to the Chaos Garden Lambda!')
#     }
