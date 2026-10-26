output "api_gateway_url" {
  description = "The invoke URL of the API Gateway endpoint for the Echo Chamber."
  value       = aws_api_gateway_stage.echo_chamber_stage.invoke_url
}

output "s3_bucket_name" {
  description = "The name of the S3 bucket used to store echoes."
  value       = aws_s3_bucket.echo_chamber_bucket.bucket
}
