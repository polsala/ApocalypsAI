output "s3_website_endpoint" {
  description = "The S3 static website endpoint URL."
  value       = aws_s3_bucket.whispering_post_bucket.website_endpoint
}

output "api_gateway_invoke_url" {
  description = "The invoke URL for the API Gateway."
  value       = aws_api_gateway_stage.whisper_api_stage.invoke_url
}
