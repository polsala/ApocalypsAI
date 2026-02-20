output "beacon_lambda_name" {
  description = "The name of the deployed AWS Lambda function."
  value       = aws_lambda_function.beacon_lambda.function_name
}

output "beacon_log_group_name" {
  description = "The name of the CloudWatch Log Group for beacon signals."
  value       = aws_cloudwatch_log_group.beacon_log_group.name
}
