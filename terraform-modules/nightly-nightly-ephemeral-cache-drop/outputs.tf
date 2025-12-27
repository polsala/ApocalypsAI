output "bucket_id" {
  description = "The ID (name) of the ephemeral cache S3 bucket."
  value       = aws_s3_bucket.ephemeral_cache.id
}

output "bucket_arn" {
  description = "The ARN of the ephemeral cache S3 bucket."
  value       = aws_s3_bucket.ephemeral_cache.arn
}
