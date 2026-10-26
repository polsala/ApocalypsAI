output "lambda_function_name" {
  description = "The name of the created Lambda function."
  value       = aws_lambda_function.hibernation_scheduler_lambda.function_name
}

output "stop_event_rule_name" {
  description = "The name of the CloudWatch Event Rule for stopping instances."
  value       = aws_cloudwatch_event_rule.stop_rule.name
}

output "start_event_rule_name" {
  description = "The name of the CloudWatch Event Rule for starting instances."
  value       = aws_cloudwatch_event_rule.start_rule.name
}
