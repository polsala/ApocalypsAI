# Production Chaos Monkey Example

# Configure providers
provider "aws" {
  region = "us-east-1"
}

# Production Chaos Monkey Module
module "chaos_monkey" {
  source = "../.."
  
  # Enable chaos engineering for production
  chaos_enabled = true
  
  # Conservative production configuration
  chaos_interval_hours = 24
  max_resources_per_run = 1
  
  # Target only non-critical resource types
  target_resource_types = [
    "aws_autoscaling_group",
    "aws_ecs_service"
  ]
  
  # Comprehensive exclusions for production
  excluded_resources = [
    "production-db-master",
    "production-db-replica",
    "production-api-gateway",
    "production-load-balancer",
    "production-cache-cluster",
    "critical-",
    "essential-",
    "master-",
    "primary-"
  ]
  
  # Dry run mode for initial testing
  dry_run = true
  
  # Production environment filtering
  environment = "production"
  
  # Advanced production settings
  max_chaos_duration_minutes = 10
  chaos_schedule_cron = "0 2 * * 1" # Weekly on Monday at 2 AM
  enable_chaos_metrics = true
  chaos_retention_days = 365
  
  # SNS topic for production notifications
  chaos_notification_topic = "arn:aws:sns:us-east-1:123456789012:production-chaos-notifications"
}

# Production test resources (these would be real resources in production)
resource "aws_autoscaling_group" "chaos_test_asg" {
  name_prefix = "chaos-test-asg-"
  max_size    = 2
  min_size    = 1
  desired_capacity = 1
  
  launch_template {
    id      = aws_launch_template.chaos_test.id
    version = "$Latest"
  }
  
  tag {
    key                 = "Environment"
    value               = "production"
    propagate_at_launch = true
  }
  
  tag {
    key                 = "Purpose"
    value               = "chaos-testing"
    propagate_at_launch = true
  }
}

resource "aws_launch_template" "chaos_test" {
  name_prefix   = "chaos-test-"
  image_id      = "ami-0c02fb55956c7d316"
  instance_type = "t3.micro"
  
  tag_specifications {
    resource_type = "instance"
    tags = {
      Environment = "production"
      Purpose     = "chaos-testing"
    }
  }
}

# Production monitoring and alerting
resource "aws_cloudwatch_metric_alarm" "chaos_events" {
  alarm_name          = "chaos-monkey-events"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "ChaosEvents"
  namespace           = "AWS/ChaosMonkey"
  period              = "300"
  statistic           = "Sum"
  threshold           = "0"
  
  alarm_description   = "Alert when chaos events occur"
  alarm_actions       = [var.chaos_notification_topic]
  
  dimensions = {
    Environment = "production"
  }
  
  tags = {
    Environment = "production"
    Purpose     = "chaos-monitoring"
  }
}

# Output production configuration
output "production_chaos_config" {
  value = {
    enabled           = module.chaos_monkey.chaos_status
    log_group         = module.chaos_monkey.chaos_log_group
    schedule          = module.chaos_monkey.chaos_schedule
    dry_run           = var.dry_run
    target_resources  = var.target_resource_types
    excluded_resources = var.excluded_resources
    metrics_enabled   = var.enable_chaos_metrics
    notifications     = var.chaos_notification_topic != ""
  }
}
