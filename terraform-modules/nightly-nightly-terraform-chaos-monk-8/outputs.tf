# Outputs
output "chaos_enabled" {
  description = "Whether chaos monkey is enabled"
  value       = var.enabled
}

output "chaos_probability" {
  description = "Current chaos probability setting"
  value       = var.chaos_probability
}

output "chaos_lambda_arn" {
  description = "ARN of the chaos monkey Lambda function"
  value       = var.enabled ? aws_lambda_function.chaos_executor[0].arn : ""
  sensitive   = true
}

output "chaos_schedule_rule" {
  description = "CloudWatch Event Rule for chaos schedule"
  value       = var.enabled ? aws_cloudwatch_event_rule.chaos_schedule[0].name : ""
}

output "chaos_log_group" {
  description = "CloudWatch Log Group for chaos monkey logs"
  value       = var.enabled ? aws_cloudwatch_log_group.chaos_logs[0].name : ""
}

output "chaos_role_arn" {
  description = "IAM Role ARN for chaos monkey Lambda"
  value       = var.enabled ? aws_iam_role.chaos_lambda_role[0].arn : ""
  sensitive   = true
}

output "chaos_policy_arn" {
  description = "IAM Policy ARN for chaos monkey Lambda"
  value       = var.enabled ? aws_iam_policy.chaos_lambda_policy[0].arn : ""
  sensitive   = true
}
