output "bucket_id" {
  description = "The ID (name) of the created S3 bucket."
  value       = aws_s3_bucket.ephemeral_bucket.id
}

output "bucket_arn" {
  description = "The ARN of the created S3 bucket."
  value       = aws_s3_bucket.ephemeral_bucket.arn
}
