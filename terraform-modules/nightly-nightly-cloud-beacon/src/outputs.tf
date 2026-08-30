output "website_endpoint" {
  description = "The domain name of the CloudFront distribution."
  value       = aws_cloudfront_distribution.beacon_distribution.domain_name
}
