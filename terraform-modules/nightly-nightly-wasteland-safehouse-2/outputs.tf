output "website_url" {
  description = "URL of the S3 static website"
  value       = aws_s3_bucket.site_bucket.website_endpoint
}

output "cloudfront_domain" {
  description = "CloudFront distribution domain name"
  value       = aws_cloudfront_distribution.cdn.domain_name
}
