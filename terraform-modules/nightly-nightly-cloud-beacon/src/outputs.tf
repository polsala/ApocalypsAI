output "s3_bucket_name" {
  description = "The name of the S3 bucket."
  value       = aws_s3_bucket.beacon_bucket.id
}

output "s3_website_endpoint" {
  description = "The S3 static website endpoint."
  value       = aws_s3_bucket.beacon_bucket.website_endpoint
}

output "cloudfront_domain_name" {
  description = "The domain name of the CloudFront distribution."
  value       = aws_cloudfront_distribution.beacon_distribution.domain_name
}

output "cloudfront_url" {
  description = "The full URL of the CloudFront distribution."
  value       = "https://${aws_cloudfront_distribution.beacon_distribution.domain_name}"
}

output "custom_domain_url" {
  description = "The custom domain URL if configured."
  value       = var.domain_name != "" ? "https://${var.domain_name}" : "N/A"
}
