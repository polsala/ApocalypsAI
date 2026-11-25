output "s3_bucket_name" {
  description = "The name of the S3 bucket where temporal logs are stored."
  value       = aws_s3_bucket.temporal_logs.bucket
}

output "lambda_function_name" {
  description = "The name of the Lambda function acting as the temporal outpost."
  value       = aws_lambda_function.temporal_outpost.function_name
}

output "cloudwatch_event_rule_name" {
  description = "The name of the CloudWatch Event Rule triggering the Lambda function."
  value       = aws_cloudwatch_event_rule.schedule.name
}
