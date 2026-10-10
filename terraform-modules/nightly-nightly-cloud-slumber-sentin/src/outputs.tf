output "slumber_lambda_arn" {
  description = "The ARN of the EC2 Slumber Manager Lambda function."
  value       = aws_lambda_function.slumber_manager.arn
}

output "stop_event_rule_arn" {
  description = "The ARN of the CloudWatch Event Rule for stopping instances."
  value       = aws_cloudwatch_event_rule.slumber_time_trigger.arn
}

output "start_event_rule_arn" {
  description = "The ARN of the CloudWatch Event Rule for starting instances."
  value       = aws_cloudwatch_event_rule.wake_up_call_trigger.arn
}
