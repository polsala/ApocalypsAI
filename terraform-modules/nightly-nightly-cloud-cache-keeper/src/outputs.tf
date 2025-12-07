output "bucket_id" {
  description = "The ID of the created S3 bucket."
  value       = aws_s3_bucket.cache_bucket.id
}

output "bucket_arn" {
  description = "The ARN of the created S3 bucket."
  value       = aws_s3_bucket.cache_bucket.arn
}

output "bucket_domain_name" {
  description = "The S3 bucket regional domain name."
  value       = aws_s3_bucket.cache_bucket.bucket_regional_domain_name
}
