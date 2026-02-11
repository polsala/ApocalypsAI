output "s3_bucket_id" {
  description = "The ID of the S3 bucket created."
  value       = aws_s3_bucket.signal_fire_bucket.id
}

output "cloudfront_domain_name" {
  description = "The domain name of the CloudFront distribution."
  value       = aws_cloudfront_distribution.signal_fire_cdn.domain_name
}

output "cloudfront_arn" {
  description = "The ARN of the CloudFront distribution."
  value       = aws_cloudfront_distribution.signal_fire_cdn.arn
}
