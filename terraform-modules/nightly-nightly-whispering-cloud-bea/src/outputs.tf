output "beacon_url" {
  description = "The URL of the deployed static website beacon."
  value       = aws_s3_bucket_website_configuration.beacon_website_config.website_endpoint
}

output "bucket_name" {
  description = "The name of the S3 bucket created for the beacon."
  value       = aws_s3_bucket.beacon_bucket.bucket
}
