output "echo_chamber_bucket_id" {
  description = "The ID of the main S3 Echo Chamber bucket."
  value       = aws_s3_bucket.echo_chamber_bucket.id
}

output "echo_chamber_bucket_arn" {
  description = "The ARN of the main S3 Echo Chamber bucket."
  value       = aws_s3_bucket.echo_chamber_bucket.arn
}

output "logging_bucket_id" {
  description = "The ID of the S3 bucket storing access logs."
  value       = aws_s3_bucket.logging_bucket.id
}

output "logging_bucket_arn" {
  description = "The ARN of the S3 bucket storing access logs."
  value       = aws_s3_bucket.logging_bucket.arn
}

output "lambda_function_arn" {
  description = "The ARN of the Lambda Echo function (if enabled)."
  value       = var.enable_lambda_echo ? aws_lambda_function.echo_chamber_lambda[0].arn : null
}

output "cloudwatch_log_group_name" {
  description = "The name of the CloudWatch Log Group for Lambda (if enabled)."
  value       = var.enable_lambda_echo ? aws_cloudwatch_log_group.lambda_echo_log_group[0].name : null
}
