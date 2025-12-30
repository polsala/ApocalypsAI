# Example: Production Environment Configuration

# This example shows how to configure the chaos monkey for a production environment
# with appropriate safety measures and monitoring.

module "chaos_monkey_production" {
  source = "./modules/chaos-monkey"
  
  # Enable chaos in production (use with extreme caution!)
  enabled = var.environment == "production"
  
  # Very low probability for production
  chaos_probability = 0.005  # 0.5% chance per hour
  
  # Target multiple resource types
  target_resource_types = [
    "aws_instance",
    "aws_rds_instance",
    "aws_elasticache_cluster"
  ]
  
  # Strict exclusions for production
  excluded_tags = {
    environment = "critical"
    team        = "ops"
    priority    = "high"
    backup      = "true"
  }
  
  # Conservative time window
  time_window_start = 10  # 10 AM
  time_window_end   = 16  # 4 PM
  
  # Keep safe mode enabled for production
  safe_mode = true
  
  # Environment-specific naming
  environment_name = "prod"
  
  # SNS topic for alerts
  alarm_sns_topic_arn = var.chaos_alerts_sns_topic_arn
}

# Example: Development Environment Configuration

module "chaos_monkey_development" {
  source = "./modules/chaos-monkey"
  
  # Always enabled in development
  enabled = true
  
  # Higher probability for testing
  chaos_probability = 0.1  # 10% chance per hour
  
  # Only target instances in dev
  target_resource_types = ["aws_instance"]
  
  # Minimal exclusions for dev
  excluded_tags = {
    environment = "protected"
  }
  
  # Extended time window for dev
  time_window_start = 8   # 8 AM
  time_window_end   = 20  # 8 PM
  
  # Safe mode can be disabled in dev for real testing
  safe_mode = false
  
  # Environment-specific naming
  environment_name = "dev"
}

# Example: Staging Environment Configuration

module "chaos_monkey_staging" {
  source = "./modules/chaos-monkey"
  
  # Enabled in staging
  enabled = true
  
  # Medium probability for staging
  chaos_probability = 0.02  # 2% chance per hour
  
  # Target instances and databases
  target_resource_types = [
    "aws_instance",
    "aws_rds_instance"
  ]
  
  # Moderate exclusions
  excluded_tags = {
    environment = "critical"
    team        = "ops"
  }
  
  # Business hours only
  time_window_start = 9   # 9 AM
  time_window_end   = 17  # 5 PM
  
  # Safe mode enabled for staging
  safe_mode = true
  
  # Environment-specific naming
  environment_name = "staging"
}

# Example: Variables for the configurations above

variable "environment" {
  description = "Current environment (production, staging, development)"
  type        = string
  default     = "development"
}

variable "chaos_alerts_sns_topic_arn" {
  description = "SNS topic ARN for chaos alerts (production only)"
  type        = string
  default     = ""
}

# Example: Outputs for monitoring

output "production_chaos_status" {
  description = "Production chaos monkey status"
  value       = module.chaos_monkey_production.chaos_enabled
}

output "development_chaos_status" {
  description = "Development chaos monkey status"
  value       = module.chaos_monkey_development.chaos_enabled
}

output "staging_chaos_status" {
  description = "Staging chaos monkey status"
  value       = module.chaos_monkey_staging.chaos_enabled
}

# Example: CloudWatch Dashboard for chaos monitoring

resource "aws_cloudwatch_dashboard" "chaos_monitoring" {
  dashboard_name = "${var.environment_name}-chaos-monitoring"
  
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
            ["ChaosMonkey", "ChaosEvents"],
            ["ChaosMonkey", "ResourcesTerminated"],
            ["ChaosMonkey", "ResourcesSkipped"],
            ["ChaosMonkey", "Errors"]
          ]
          period = 3600
          stat   = "Sum"
          region = "us-east-1"
          title  = "Chaos Monkey Metrics"
        }
      },
      {
        type   = "log"
        x      = 0
        y      = 6
        width  = 24
        height = 9
        properties = {
          query    = "SOURCE '/aws/lambda/${module.chaos_monkey_production.chaos_lambda_arn}' | fields @timestamp, message | sort @timestamp desc | limit 100"
          region   = "us-east-1"
          logGroup = module.chaos_monkey_production.chaos_log_group
          title    = "Chaos Monkey Logs"
        }
      }
    ]
  })
}
