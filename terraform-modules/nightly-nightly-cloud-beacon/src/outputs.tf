output "website_endpoint" {
  description = "The URL of the deployed static website beacon."
  value       = aws_s3_bucket_website_configuration.beacon_website.website_endpoint
}

output "bucket_name" {
  description = "The name of the S3 bucket created."
  value       = aws_s3_bucket.beacon_bucket.bucket
}
