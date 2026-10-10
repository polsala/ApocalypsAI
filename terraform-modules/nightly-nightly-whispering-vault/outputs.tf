output "bucket_id" {
  description = "The ID (name) of the created S3 bucket."
  value       = aws_s3_bucket.whisper_vault.id
}

output "bucket_arn" {
  description = "The ARN (Amazon Resource Name) of the created S3 bucket."
  value       = aws_s3_bucket.whisper_vault.arn
}
