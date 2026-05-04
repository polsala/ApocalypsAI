output "cloudfront_domain_name" {
  description = "The domain name of the CloudFront distribution."
  value       = aws_cloudfront_distribution.echo_chamber_cdn.domain_name
}

output "s3_bucket_website_endpoint" {
  description = "The S3 static website endpoint (for direct access, not recommended)."
  value       = aws_s3_bucket_website_configuration.echo_chamber_website.website_endpoint
}
