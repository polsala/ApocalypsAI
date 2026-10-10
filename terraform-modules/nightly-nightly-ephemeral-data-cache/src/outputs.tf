output "s3_bucket_id" {
  description = "The ID (name) of the S3 bucket."
  value       = aws_s3_bucket.ephemeral_cache.id
}

output "s3_bucket_arn" {
  description = "The ARN of the S3 bucket."
  value       = aws_s3_bucket.ephemeral_cache.arn
}
