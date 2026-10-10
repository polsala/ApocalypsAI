output "s3_bucket_name" {
  description = "The name of the S3 bucket hosting the beacon content."
  value       = aws_s3_bucket.beacon_bucket.id
}

output "cloudfront_domain_name" {
  description = "The domain name of the CloudFront distribution for the beacon."
  value       = aws_cloudfront_distribution.beacon_cdn.domain_name
}

output "cloudfront_url" {
  description = "The full URL of the CloudFront distribution."
  value       = "https://${aws_cloudfront_distribution.beacon_cdn.domain_name}"
}
