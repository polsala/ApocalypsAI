output "chaos_garden_url" {
  description = "URL to access the chaos garden dashboard"
  value       = "https://${aws_api_gateway_rest_api.chaos_garden_api.id}.execute-api.${var.region}.amazonaws.com/prod/experiments"
}

output "experiment_results_bucket" {
  description = "S3 bucket containing experiment results and logs"
  value       = aws_s3_bucket.chaos_logs.id
}

output "monitoring_dashboard_url" {
  description = "CloudWatch dashboard URL for monitoring chaos experiments"
  value       = "https://console.aws.amazon.com/cloudwatch/home?region=${var.region}#alarmsV2:alarm/${aws_cloudwatch_metric_alarm.chaos_failure_alarm.alarm_name}"
}

output "sns_topic_arn" {
  description = "ARN of the SNS topic for chaos alerts"
  value       = aws_sns_topic.chaos_alerts.arn
}

output "lambda_function_arn" {
  description = "ARN of the chaos orchestrator Lambda function"
  value       = aws_lambda_function.chaos_orchestrator.arn
}

output "api_gateway_id" {
  description = "API Gateway ID for the chaos garden"
  value       = aws_api_gateway_rest_api.chaos_garden_api.id
}

output "event_rule_name" {
  description = "EventBridge rule name for chaos experiment scheduling"
  value       = aws_cloudwatch_event_rule.chaos_schedule.name
}
