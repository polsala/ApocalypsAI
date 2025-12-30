output "bucket_arn" {
  description = "ARN of the created S3 bucket"
  value       = aws_s3_bucket.shelter.arn
}

output "cloudfront_domain_name" {
  description = "Domain name of the CloudFront distribution"
  value       = aws_cloudfront_distribution.shelter.domain_name
}
