output "bucket_id" {
  description = "The ID of the created S3 bucket."
  value       = aws_s3_bucket.static_site.id
}

output "bucket_arn" {
  description = "The ARN of the created S3 bucket."
  value       = aws_s3_bucket.static_site.arn
}

output "cloudfront_domain" {
  description = "The domain name of the CloudFront distribution (if enabled)."
  value       = aws_cloudfront_distribution.cdn[0].domain_name
  condition   = var.enable_cdn
}
