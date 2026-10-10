output "s3_bucket_id" {
  description = "The ID of the S3 bucket created."
  value       = aws_s3_bucket.beacon_bucket.id
}

output "cloudfront_domain_name" {
  description = "The domain name of the CloudFront distribution."
  value       = aws_cloudfront_distribution.beacon_distribution.domain_name
}

output "cloudfront_distribution_id" {
  description = "The ID of the CloudFront distribution."
  value       = aws_cloudfront_distribution.beacon_distribution.id
}
