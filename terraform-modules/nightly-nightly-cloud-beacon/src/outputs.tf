output "website_endpoint" {
  description = "The S3 static website endpoint URL."
  value       = aws_s3_bucket_website_configuration.beacon_website_config.website_endpoint
}

output "cloudfront_domain_name" {
  description = "The CloudFront distribution domain name."
  value       = aws_cloudfront_distribution.beacon_cdn.domain_name
}

output "cloudfront_zone_id" {
  description = "The CloudFront distribution hosted zone ID."
  value       = aws_cloudfront_distribution.beacon_cdn.hosted_zone_id
}
