output "s3_bucket_id" {
  description = "The ID (name) of the created S3 bucket."
  value       = aws_s3_bucket.vault.id
}

output "s3_bucket_arn" {
  description = "The ARN (Amazon Resource Name) of the S3 bucket."
  value       = aws_s3_bucket.vault.arn
}
