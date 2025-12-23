output "bucket_arn" {
  description = "ARN of the created S3 bucket"
  value       = aws_s3_bucket.static_site.arn
}

output "website_endpoint" {
  description = "S3 website endpoint URL"
  value       = aws_s3_bucket.static_site.website_endpoint
}

output "cloudfront_domain" {
  description = "Domain name of the CloudFront distribution (empty if disabled)"
  value       = var.enable_cloudfront ? aws_cloudfront_distribution.cdn[0].domain_name : ""
}
