# This file is intentionally empty
# The main module configuration is in the root directory
# This module serves as a wrapper for the root configuration

# Include all root module files
terraform {
  source = "../.."
}

# Pass through all variables
variable "prefix" {}
variable "enabled" {}
variable "region" {}
variable "chaos_schedule" {}
variable "chaos_intensity" {}
variable "target_resources" {}
variable "safe_mode" {}
variable "excluded_tags" {}
variable "log_retention_days" {}
variable "max_terminations_per_run" {}
variable "min_time_between_runs" {}
variable "notification_emails" {}
variable "enable_notifications" {}
variable "chaos_window_start" {}
variable "chaos_window_end" {}
variable "enable_metrics" {}
variable "enable_alarm" {}
variable "custom_chaos_script" {}
variable "dry_run_only" {}
variable "chaos_tags" {}
variable "excluded_resource_ids" {}
variable "chaos_duration_minutes" {}

# Include all outputs
output "chaos_lambda_arn" {}
output "chaos_lambda_name" {}
output "chaos_sns_topic_arn" {}
output "chaos_sns_topic_name" {}
output "chaos_schedule_rule" {}
output "chaos_schedule_expression" {}
output "chaos_dashboard_name" {}
output "chaos_dashboard_url" {}
output "chaos_intensity" {}
output "chaos_target_resources" {}
output "chaos_safe_mode" {}
output "chaos_excluded_tags" {}
output "chaos_enabled" {}
output "chaos_log_retention" {}
output "chaos_notifications_enabled" {}
output "chaos_metrics_enabled" {}
output "chaos_alarm_enabled" {}
output "total_resources_targeted" {}
output "excluded_tags_count" {}
output "notification_emails_count" {}
output "chaos_iam_role_arn" {}
output "chaos_iam_policy_arn" {}
output "chaos_window" {}
output "chaos_max_terminations" {}
output "chaos_min_time_between_runs" {}
output "chaos_duration_limit" {}
output "chaos_tags" {}
output "excluded_resource_ids_count" {}
output "chaos_dry_run_only" {}
