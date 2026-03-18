output "lambda_function_name" {
  description = "The name of the deployed AWS Lambda function."
  value       = aws_lambda_function.temporal_beacon.function_name
}

output "cloudwatch_log_group_name" {
  description = "The name of the CloudWatch Log Group where beacon messages are sent."
  value       = aws_cloudwatch_log_group.beacon_log_group.name
}
