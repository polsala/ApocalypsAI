output "cloudfront_domain_name" {
  description = "The domain name of the CloudFront distribution, where your beacon will be accessible."
  value       = aws_cloudfront_distribution.s3_distribution.domain_name
}

output "s3_bucket_name" {
  description = "The name of the S3 bucket hosting the beacon content."
  value       = aws_s3_bucket.content_bucket.id
}
