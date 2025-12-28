# Local values for common configurations
locals {
  # Resource naming conventions
  chaos_lambda_name    = "${var.prefix}-chaos-monkey"
  chaos_role_name      = "${var.prefix}-chaos-lambda-role"
  chaos_policy_name    = "${var.prefix}-chaos-lambda-policy"
  chaos_schedule_name  = "${var.prefix}-chaos-schedule"
  chaos_sns_topic_name = "${var.prefix}-chaos-notifications"
  chaos_log_group_name = "/aws/lambda/${local.chaos_lambda_name}"
  chaos_dashboard_name = "${var.prefix}-chaos-dashboard"
  chaos_alarm_name     = "${var.prefix}-chaos-failures"
  
  # Tag map for all chaos-related resources
  chaos_tags = merge(
    var.chaos_tags,
    {
      "Name"              = "${var.prefix}-chaos-monkey"
      "Environment"       = "${var.prefix}"
      "ManagedBy"         = "terraform"
      "Project"           = "chaos-monkey"
      "Terraform"         = "true"
      "ChaosMonkey"       = "enabled"
    }
  )
  
  # Lambda environment variables
  lambda_env_vars = {
    CHAOS_INTENSITY    = var.chaos_intensity
    TARGET_RESOURCES = jsonencode(var.target_resources)
    EXCLUDED_TAGS    = jsonencode(var.excluded_tags)
    SAFE_MODE        = var.safe_mode
    REGION           = var.region
    SNS_TOPIC_ARN    = aws_sns_topic.chaos_notifications.arn
    MAX_TERMINATIONS = var.max_terminations_per_run
    CHAOS_WINDOW_START = var.chaos_window_start
    CHAOS_WINDOW_END   = var.chaos_window_end
    DRY_RUN_ONLY       = var.dry_run_only
    EXCLUDED_RESOURCE_IDS = jsonencode(var.excluded_resource_ids)
  }
  
  # CloudWatch Event schedule validation
  schedule_valid = contains([
    "rate(1 minute)",
    "rate(5 minutes)",
    "rate(1 hour)",
    "rate(1 day)",
    "cron(* * * * ? *)",
    "cron(0 * * * ? *)",
    "cron(0 */6 * * ? *)",
    "cron(0 2 * * ? *)"
  ], var.chaos_schedule)
  
  # Resource type mappings
  resource_type_mapping = {
    "aws_instance"      = "EC2 Instance"
    "aws_rds_instance"  = "RDS Instance"
    "aws_ecs_service"   = "ECS Service"
    "aws_autoscaling_group" = "Auto Scaling Group"
    "aws_elasticache_cluster" = "ElastiCache Cluster"
  }
  
  # Chaos intensity validation
  intensity_valid = var.chaos_intensity >= 0 && var.chaos_intensity <= 100
  
  # Safe mode warning
  safe_mode_warning = var.safe_mode ? "[WARNING: Safe mode is enabled - no actual resource termination will occur]" : ""
  
  # Notification configuration
  notification_config = {
    enabled = var.enable_notifications
    emails  = var.notification_emails
    topic_arn = aws_sns_topic.chaos_notifications.arn
  }
  
  # Metrics configuration
  metrics_config = {
    enabled = var.enable_metrics
    dashboard_name = local.chaos_dashboard_name
    alarm_enabled = var.enable_alarm
    alarm_name = local.chaos_alarm_name
  }
  
  # Chaos window validation
  window_valid = var.chaos_window_start < var.chaos_window_end
  
  # Duration validation
  duration_valid = var.chaos_duration_minutes > 0 && var.chaos_duration_minutes <= 1440
  
  # Excluded tags validation
  excluded_tags_valid = length(var.excluded_tags) > 0
  
  # Target resources validation
  target_resources_valid = length(var.target_resources) > 0
  
  # Combined validation status
  validation_status = {
    all_valid = local.intensity_valid &&
                local.window_valid &&
                local.duration_valid &&
                local.excluded_tags_valid &&
                local.target_resources_valid
    issues = [
      for issue in [
        local.intensity_valid ? "" : "Invalid chaos intensity",
        local.window_valid ? "" : "Invalid chaos window",
        local.duration_valid ? "" : "Invalid chaos duration",
        local.excluded_tags_valid ? "" : "No excluded tags configured",
        local.target_resources_valid ? "" : "No target resources configured"
      ]
      if issue != ""
    ]
  }
}

# Validation rules
validation {
  condition     = local.validation_status.all_valid
  error_message = "Chaos Monkey configuration has validation errors: ${join(", ", local.validation_status.issues)}"
}

# Additional local validations
validation {
  condition     = var.chaos_intensity > 0 || var.safe_mode
  error_message = "Chaos intensity must be greater than 0, or safe mode must be enabled."
}

validation {
  condition     = var.max_terminations_per_run > 0
  error_message = "Maximum terminations per run must be greater than 0."
}

validation {
  condition     = var.min_time_between_runs > 0
  error_message = "Minimum time between runs must be greater than 0."
}

validation {
  condition     = var.log_retention_days in [1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1827, 3653]
  error_message = "Log retention days must be one of: 1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1827, 3653."
}

# Warning for production use
warning "production_warning" {
  condition     = !var.safe_mode && !var.dry_run_only
  summary       = "Production Chaos Warning"
  detail        = "Chaos Monkey is configured to perform actual resource termination. Ensure this is intended for your environment."
}

# Warning for high chaos intensity
warning "high_intensity_warning" {
  condition     = var.chaos_intensity > 50
  summary       = "High Chaos Intensity Warning"
  detail        = "Chaos intensity is set above 50%. This may cause significant service disruption."
}

# Warning for short time between runs
warning "frequent_runs_warning" {
  condition     = var.min_time_between_runs < 6
  summary       = "Frequent Chaos Runs Warning"
  detail        = "Chaos runs are scheduled more frequently than every 6 hours. This may impact system stability."
}
