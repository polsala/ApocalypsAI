output "bucket_id" {
  description = "The ID of the created S3 bucket."
  value       = aws_s3_bucket.static_site.id
}

output "bucket_arn" {
  description = "The ARN of the created S3 bucket."
  value       = aws_s3_bucket.static_site.arn
}

output "website_endpoint" {
  description = "The website endpoint URL."
  value       = aws_s3_bucket.static_site.website_endpoint
}
