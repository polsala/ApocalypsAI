# Production Chaos Monkey Example

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

# Production Chaos Monkey configuration
module "chaos_monkey" {
  source = "../.."
  
  # Production configuration
  prefix = "prod-chaos"
  enabled = true
  
  # Conservative chaos settings
  chaos_schedule = "0 3 * * 1"  # Weekly on Monday at 3 AM
  chaos_intensity = 2           # 2% of resources
  safe_mode = false            # Actual termination enabled
  dry_run_only = false         # Real chaos
  
  # Target resources
  target_resources = [
    "aws_instance",
    "aws_rds_instance",
    "aws_ecs_service",
    "aws_autoscaling_group"
  ]
  
  # Strict excluded tags
  excluded_tags = [
    "critical",
    "production-critical",
    "do-not-terminate",
    "database-primary",
    "load-balancer",
    "monitoring"
  ]
  
  # Production logging
  log_retention_days = 90
  
  # Conservative limits
  max_terminations_per_run = 3
  min_time_between_runs = 168  # 1 week
  
  # Production notifications
  enable_notifications = true
  notification_emails = [
    "platform-team@example.com",
    "oncall@example.com"
  ]
  
  # Production metrics and monitoring
  enable_metrics = true
  enable_alarm = true
  
  # Production chaos window
  chaos_window_start = 2
  chaos_window_end = 6
  
  # Production duration limit
  chaos_duration_minutes = 60
  
  # Production tags
  chaos_tags = {
    "Environment" = "production"
    "Team"       = "platform"
    "CostCenter" = "platform-ops"
  }
  
  # Specifically excluded resource IDs
  excluded_resource_ids = [
    "i-1234567890abcdef0",  # Primary database
    "i-0987654321fedcba0"   # Load balancer
  ]
}

# Output production information
output "production_chaos_status" {
  description = "Production Chaos Monkey status"
  value = {
    enabled = module.chaos_monkey.chaos_enabled
    intensity = module.chaos_monkey.chaos_intensity
    safe_mode = module.chaos_monkey.chaos_safe_mode
    dry_run_only = module.chaos_monkey.chaos_dry_run_only
    targets = module.chaos_monkey.chaos_target_resources
    dashboard_url = module.chaos_monkey.chaos_dashboard_url
    notification_emails = module.chaos_monkey.notification_emails_count
    excluded_tags = module.chaos_monkey.chaos_excluded_tags
  }
}

# Additional production resources
resource "aws_sns_topic_subscription" "chaos_notifications" {
  topic_arn = module.chaos_monkey.chaos_sns_topic_arn
  protocol  = "email"
  endpoint  = "platform-team@example.com"
}

resource "aws_sns_topic_subscription" "chaos_oncall" {
  topic_arn = module.chaos_monkey.chaos_sns_topic_arn
  protocol  = "email"
  endpoint  = "oncall@example.com"
}

# Production alerting
resource "aws_cloudwatch_metric_alarm" "chaos_high_error_rate" {
  alarm_name          = "prod-chaos-high-error-rate"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = "300"
  statistic           = "Sum"
  threshold           = "5"
  alarm_description   = "High error rate in Chaos Monkey executions"
  alarm_actions       = [module.chaos_monkey.chaos_sns_topic_arn]
  dimensions = {
    FunctionName = module.chaos_monkey.chaos_lambda_name
  }
}

# Production dashboard enhancements
resource "aws_cloudwatch_dashboard" "production_chaos_dashboard" {
  dashboard_name = "prod-chaos-enhanced-dashboard"
  
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
            ["AWS/Lambda", "Invocations", "FunctionName", module.chaos_monkey.chaos_lambda_name],
            ["AWS/Lambda", "Errors", "FunctionName", module.chaos_monkey.chaos_lambda_name],
            ["AWS/Lambda", "Duration", "FunctionName", module.chaos_monkey.chaos_lambda_name]
          ]
          period = 300
          stat   = "Average"
          region = "us-east-1"
          title  = "Chaos Monkey Execution Metrics"
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
            ["AWS/Lambda", "Throttles", "FunctionName", module.chaos_monkey.chaos_lambda_name],
            ["AWS/Lambda", "ConcurrentExecutions", "FunctionName", module.chaos_monkey.chaos_lambda_name]
          ]
          period = 300
          stat   = "Sum"
          region = "us-east-1"
          title  = "Chaos Monkey Performance Metrics"
        }
      },
      {
        type   = "log"
        x      = 0
        y      = 6
        width  = 24
        height = 6
        properties = {
          query = "SOURCE '${module.chaos_monkey.chaos_log_retention}'
| fields @timestamp, @message
| filter @message like /chaos/
| sort @timestamp desc
| limit 200"
          region = "us-east-1"
          title  = "Chaos Monkey Detailed Logs"
        }
      }
    ]
  })
}

# Output enhanced production information
output "production_chaos_enhanced" {
  description = "Enhanced production Chaos Monkey information"
  value = {
    enhanced_dashboard_url = "https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#dashboards:name=${aws_cloudwatch_dashboard.production_chaos_dashboard.dashboard_name}"
    sns_subscriptions = [
      aws_sns_topic_subscription.chaos_notifications.arn,
      aws_sns_topic_subscription.chaos_oncall.arn
    ]
    error_alarm = aws_cloudwatch_metric_alarm.chaos_high_error_rate.alarm_name
  }
}
