output "s3_bucket_endpoint" {
  description = "The S3 static website endpoint URL."
  value       = aws_s3_bucket_website_configuration.waypoint_content.website_endpoint
}

output "cloudfront_domain_name" {
  description = "The domain name of the deployed CloudFront distribution."
  value       = aws_cloudfront_distribution.waypoint_cdn.domain_name
}
