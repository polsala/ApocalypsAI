# Development Chaos Monkey Example

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
  region = "us-east-1"
}

# Development Chaos Monkey configuration
module "chaos_monkey" {
  source = "../.."
  
  # Development configuration
  prefix = "dev-chaos"
  enabled = true
  
  # Frequent chaos for development
  chaos_schedule = "0 */2 * * *"  # Every 2 hours
  chaos_intensity = 20            # 20% of resources
  safe_mode = true               # Always safe mode in dev
  dry_run_only = true            # Only dry runs
  
  # All resource types
  target_resources = [
    "aws_instance",
    "aws_rds_instance",
    "aws_ecs_service",
    "aws_autoscaling_group",
    "aws_elasticache_cluster"
  ]
  
  # Minimal excluded tags
  excluded_tags = [
    "do-not-terminate"
  ]
  
  # Short log retention
  log_retention_days = 3
  
  # High limits for development
  max_terminations_per_run = 20
  min_time_between_runs = 1
  
  # Development notifications
  enable_notifications = false
  
  # Development metrics
  enable_metrics = true
  enable_alarm = false
  
  # Flexible chaos window
  chaos_window_start = 0
  chaos_window_end = 23
  
  # Short duration
  chaos_duration_minutes = 10
  
  # Development tags
  chaos_tags = {
    "Environment" = "development"
    "Team"       = "dev-team"
  }
}

# Output development information
output "development_chaos_status" {
  description = "Development Chaos Monkey status"
  value = {
    enabled = module.chaos_monkey.chaos_enabled
    intensity = module.chaos_monkey.chaos_intensity
    safe_mode = module.chaos_monkey.chaos_safe_mode
    dry_run_only = module.chaos_monkey.chaos_dry_run_only
    targets = module.chaos_monkey.chaos_target_resources
    dashboard_url = module.chaos_monkey.chaos_dashboard_url
    chaos_window = module.chaos_monkey.chaos_window
    max_terminations = module.chaos_monkey.chaos_max_terminations
  }
}

# Development-specific resources
resource "aws_cloudwatch_metric_alarm" "chaos_dev_test_alarm" {
  count              = 0  # Disabled in development
  alarm_name          = "dev-chaos-test-alarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = "300"
  statistic           = "Sum"
  threshold           = "1"
  alarm_description   = "Test alarm for development"
  alarm_actions       = [module.chaos_monkey.chaos_sns_topic_arn]
  dimensions = {
    FunctionName = module.chaos_monkey.chaos_lambda_name
  }
}

# Development dashboard
resource "aws_cloudwatch_dashboard" "development_chaos_dashboard" {
  dashboard_name = "dev-chaos-dashboard"
  
  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 24
        height = 6
        properties = {
          metrics = [
            ["AWS/Lambda", "Invocations", "FunctionName", module.chaos_monkey.chaos_lambda_name],
            ["AWS/Lambda", "Errors", "FunctionName", module.chaos_monkey.chaos_lambda_name]
          ]
          period = 300
          stat   = "Sum"
          region = "us-east-1"
          title  = "Development Chaos Monkey Metrics"
        }
      },
      {
        type   = "text"
        x      = 0
        y      = 6
        width  = 24
        height = 3
        properties = {
          markdown = "# Development Chaos Monkey\n\nThis is a development environment. All chaos events are in safe mode and dry run only.\n\n**Schedule**: Every 2 hours\n**Intensity**: 20%\n**Safe Mode**: Enabled\n**Dry Run**: Enabled"
        }
      }
    ]
  })
}

# Output development dashboard
output "development_dashboard_url" {
  description = "Development Chaos Monkey dashboard URL"
  value       = "https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#dashboards:name=${aws_cloudwatch_dashboard.development_chaos_dashboard.dashboard_name}"
}
