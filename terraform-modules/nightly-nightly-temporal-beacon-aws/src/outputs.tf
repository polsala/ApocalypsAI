output "s3_bucket_name" {
  description = "The name of the S3 bucket created."
  value       = aws_s3_bucket.anomaly_logs.bucket
}

output "lambda_function_name" {
  description = "The name of the Lambda function created."
  value       = aws_lambda_function.anomaly_handler.function_name
}

output "lambda_invoke_arn" {
  description = "The ARN to invoke the Lambda function."
  value       = aws_lambda_function.anomaly_handler.invoke_arn
}
