output "cloudfront_domain_name" {
  description = "The domain name of the CloudFront distribution."
  value       = aws_cloudfront_distribution.beacon_cdn.domain_name
}

output "s3_bucket_website_endpoint" {
  description = "The S3 static website endpoint URL."
  value       = aws_s3_bucket.beacon_bucket.website_endpoint
}

output "s3_bucket_id" {
  description = "The ID of the S3 bucket."
  value       = aws_s3_bucket.beacon_bucket.id
}
