output "bucket_id" {
  description = "The ID of the created S3 bucket."
  value       = aws_s3_bucket.temporal_vault.id
}

output "bucket_arn" {
  description = "The ARN of the created S3 bucket."
  value       = aws_s3_bucket.temporal_vault.arn
}

output "bucket_name" {
  description = "The name of the created S3 bucket."
  value       = aws_s3_bucket.temporal_vault.bucket
}
