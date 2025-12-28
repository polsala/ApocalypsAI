# Basic test configuration
basic_config = {
  prefix = "test-chaos"
  enabled = true
  chaos_schedule = "0 2 * * *"
  chaos_intensity = 5
  safe_mode = true
  target_resources = ["aws_instance"]
  excluded_tags = ["critical", "production-critical"]
  log_retention_days = 7
  max_terminations_per_run = 5
  min_time_between_runs = 6
  enable_notifications = true
  notification_emails = ["admin@example.com"]
  enable_metrics = true
  enable_alarm = true
  chaos_window_start = 2
  chaos_window_end = 6
  chaos_duration_minutes = 30
  chaos_tags = {
    "Environment" = "test"
    "Team"       = "platform"
  }
}

# Production test configuration
production_config = {
  prefix = "prod-test-chaos"
  enabled = true
  chaos_schedule = "0 3 * * 1"
  chaos_intensity = 2
  safe_mode = false
  target_resources = ["aws_instance", "aws_rds_instance"]
  excluded_tags = ["critical", "production-critical", "do-not-terminate", "database-primary", "load-balancer"]
  log_retention_days = 90
  max_terminations_per_run = 3
  min_time_between_runs = 168
  enable_notifications = true
  notification_emails = ["platform-team@example.com", "oncall@example.com"]
  enable_metrics = true
  enable_alarm = true
  chaos_window_start = 2
  chaos_window_end = 6
  chaos_duration_minutes = 60
  chaos_tags = {
    "Environment" = "production"
    "Team"       = "platform"
    "CostCenter" = "platform-ops"
  }
  excluded_resource_ids = ["i-1234567890abcdef0", "i-0987654321fedcba0"]
}

# Development test configuration
development_config = {
  prefix = "dev-test-chaos"
  enabled = true
  chaos_schedule = "0 */2 * * *"
  chaos_intensity = 20
  safe_mode = true
  dry_run_only = true
  target_resources = ["aws_instance", "aws_rds_instance", "aws_ecs_service", "aws_autoscaling_group", "aws_elasticache_cluster"]
  excluded_tags = ["do-not-terminate"]
  log_retention_days = 3
  max_terminations_per_run = 20
  min_time_between_runs = 1
  enable_notifications = false
  notification_emails = []
  enable_metrics = true
  enable_alarm = false
  chaos_window_start = 0
  chaos_window_end = 23
  chaos_duration_minutes = 10
  chaos_tags = {
    "Environment" = "development"
    "Team"       = "dev-team"
  }
}

# High intensity test configuration
high_intensity_config = {
  prefix = "high-intensity-chaos"
  enabled = true
  chaos_schedule = "0 0 * * *"
  chaos_intensity = 100
  safe_mode = false
  target_resources = ["aws_instance"]
  excluded_tags = []
  log_retention_days = 1
  max_terminations_per_run = 100
  min_time_between_runs = 1
  enable_notifications = false
  notification_emails = []
  enable_metrics = false
  enable_alarm = false
  chaos_window_start = 0
  chaos_window_end = 23
  chaos_duration_minutes = 5
  chaos_tags = {
    "Environment" = "test"
    "Team"       = "chaos-testing"
  }
}

# Zero intensity test configuration
zero_intensity_config = {
  prefix = "zero-intensity-chaos"
  enabled = true
  chaos_schedule = "0 0 * * *"
  chaos_intensity = 0
  safe_mode = true
  target_resources = ["aws_instance"]
  excluded_tags = []
  log_retention_days = 1
  max_terminations_per_run = 1
  min_time_between_runs = 1
  enable_notifications = false
  notification_emails = []
  enable_metrics = false
  enable_alarm = false
  chaos_window_start = 0
  chaos_window_end = 23
  chaos_duration_minutes = 5
  chaos_tags = {
    "Environment" = "test"
    "Team"       = "chaos-testing"
  }
}

# Disabled test configuration
disabled_config = {
  prefix = "disabled-chaos"
  enabled = false
  chaos_schedule = "0 0 * * *"
  chaos_intensity = 5
  safe_mode = true
  target_resources = ["aws_instance"]
  excluded_tags = []
  log_retention_days = 7
  max_terminations_per_run = 5
  min_time_between_runs = 6
  enable_notifications = false
  notification_emails = []
  enable_metrics = false
  enable_alarm = false
  chaos_window_start = 0
  chaos_window_end = 23
  chaos_duration_minutes = 30
  chaos_tags = {
    "Environment" = "test"
    "Team"       = "chaos-testing"
  }
}

# Multi-region test configuration
multi_region_config = {
  prefix = "multi-region-chaos"
  enabled = true
  chaos_schedule = "0 0 * * *"
  chaos_intensity = 10
  safe_mode = true
  target_resources = ["aws_instance", "aws_rds_instance", "aws_ecs_service"]
  excluded_tags = ["critical"]
  log_retention_days = 7
  max_terminations_per_run = 10
  min_time_between_runs = 12
  enable_notifications = true
  notification_emails = ["admin@example.com"]
  enable_metrics = true
  enable_alarm = true
  chaos_window_start = 1
  chaos_window_end = 5
  chaos_duration_minutes = 15
  chaos_tags = {
    "Environment" = "multi-region"
    "Team"       = "platform"
  }
}

# Custom script test configuration
# Note: This would require a custom_chaos_script file
# custom_script_config = {
#   prefix = "custom-script-chaos"
#   enabled = true
#   chaos_schedule = "0 0 * * *"
#   chaos_intensity = 5
#   safe_mode = true
#   target_resources = ["aws_instance"]
#   excluded_tags = []
#   log_retention_days = 7
#   max_terminations_per_run = 5
#   min_time_between_runs = 6
#   enable_notifications = false
#   notification_emails = []
#   enable_metrics = false
#   enable_alarm = false
#   chaos_window_start = 0
#   chaos_window_end = 23
#   chaos_duration_minutes = 30
#   chaos_tags = {
#     "Environment" = "test"
#     "Team"       = "chaos-testing"
#   }
#   custom_chaos_script = "./custom_chaos_script.py"
# }
