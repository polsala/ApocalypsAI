output "s3_bucket_id" {
  description = "The ID of the S3 bucket."
  value       = aws_s3_bucket.wasteland_cache.id
}

output "s3_bucket_arn" {
  description = "The ARN of the S3 bucket."
  value       = aws_s3_bucket.wasteland_cache.arn
}

output "s3_bucket_domain_name" {
  description = "The domain name of the S3 bucket."
  value       = aws_s3_bucket.wasteland_cache.bucket_domain_name
}
