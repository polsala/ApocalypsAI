output "lambda_function_name" {
  description = "The name of the deployed AWS Lambda function."
  value       = aws_lambda_function.constellation_mapper.function_name
}

output "s3_data_bucket_name" {
  description = "The name of the S3 bucket storing constellation map data."
  value       = aws_s3_bucket.constellation_data_bucket.bucket
}
