# Outputs
output "chaos_lambda_arn" {
  description = "ARN of the chaos monkey Lambda function"
  value       = aws_lambda_function.chaos_monkey.arn
  sensitive   = false
}

output "chaos_schedule_rule" {
  description = "CloudWatch Events rule name for chaos schedule"
  value       = aws_cloudwatch_event_rule.chaos_schedule.name
  sensitive   = false
}

output "chaos_notifications_topic" {
  description = "SNS topic ARN for chaos notifications"
  value       = var.enable_notifications ? aws_sns_topic.chaos_notifications[0].arn : ""
  sensitive   = true
}

output "module_enabled" {
  description = "Whether the chaos monkey is enabled"
  value       = var.enabled
  sensitive   = false
}

output "chaos_lambda_name" {
  description = "Name of the chaos monkey Lambda function"
  value       = aws_lambda_function.chaos_monkey.function_name
  sensitive   = false
}

output "chaos_schedule_expression" {
  description = "CloudWatch Events schedule expression"
  value       = var.chaos_schedule
  sensitive   = false
}

output "chaos_log_group" {
  description = "CloudWatch Log Group for chaos monkey logs"
  value       = aws_cloudwatch_log_group.chaos_lambda_logs.name
  sensitive   = false
}
