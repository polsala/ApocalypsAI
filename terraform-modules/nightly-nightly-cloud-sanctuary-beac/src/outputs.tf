output "cloudfront_domain_name" {
  description = "The domain name of the CloudFront distribution."
  value       = aws_cloudfront_distribution.beacon_cdn.domain_name
}

output "s3_bucket_name" {
  description = "The name of the S3 bucket hosting the content."
  value       = aws_s3_bucket.beacon_bucket.bucket
}
