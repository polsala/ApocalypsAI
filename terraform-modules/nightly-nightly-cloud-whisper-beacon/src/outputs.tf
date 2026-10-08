output "cloudfront_domain_name" {
  description = "The domain name of the CloudFront distribution for the beacon."
  value       = aws_cloudfront_distribution.beacon_distribution.domain_name
}

output "s3_bucket_website_endpoint" {
  description = "The S3 static website endpoint."
  value       = aws_s3_bucket_website_configuration.beacon_website.website_endpoint
}
