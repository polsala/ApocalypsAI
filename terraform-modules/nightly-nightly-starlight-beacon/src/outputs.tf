output "s3_bucket_id" {
  description = "The ID of the S3 bucket."
  value       = aws_s3_bucket.website_bucket.id
}

output "s3_bucket_regional_domain_name" {
  description = "The regional domain name of the S3 bucket."
  value       = aws_s3_bucket.website_bucket.bucket_regional_domain_name
}

output "cloudfront_domain_name" {
  description = "The domain name of the CloudFront distribution."
  value       = aws_cloudfront_distribution.website_cdn.domain_name
}

output "cloudfront_hosted_zone_id" {
  description = "The CloudFront Hosted Zone ID."
  value       = aws_cloudfront_distribution.website_cdn.hosted_zone_id
}
