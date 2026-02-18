output "s3_website_endpoint" {
  description = "The S3 static website endpoint."
  value       = aws_s3_bucket.temporal_anchor_bucket.website_endpoint
}

output "cloudfront_domain_name" {
  description = "The domain name of the CloudFront distribution."
  value       = aws_cloudfront_distribution.temporal_anchor_cdn.domain_name
}

output "cloudfront_arn" {
  description = "The ARN of the CloudFront distribution."
  value       = aws_cloudfront_distribution.temporal_anchor_cdn.arn
}
