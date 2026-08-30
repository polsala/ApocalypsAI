output "bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.website.arn
}

output "website_endpoint" {
  description = "Website endpoint URL"
  value       = aws_s3_bucket.website.website_endpoint
}

output "cloudfront_distribution_id" {
  description = "ID of CloudFront distribution (if created)"
  value       = var.enable_cloudfront ? aws_cloudfront_distribution.cdn[0].id : null
}
