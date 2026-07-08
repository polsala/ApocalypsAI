output "cloudfront_domain_name" {
  description = "The domain name of the AWS CloudFront distribution."
  value       = aws_cloudfront_distribution.beacon.domain_name
}

output "s3_bucket_website_endpoint" {
  description = "The S3 static website endpoint (without CloudFront)."
  value       = aws_s3_bucket_website_configuration.beacon.website_endpoint
}
