output "bucket_id" {
  description = "The ID (name) of the created S3 bucket."
  value       = aws_s3_bucket.cosmic_dust.id
}

output "bucket_arn" {
  description = "The ARN of the created S3 bucket."
  value       = aws_s3_bucket.cosmic_dust.arn
}

output "bucket_domain_name" {
  description = "The domain name of the created S3 bucket."
  value       = aws_s3_bucket.cosmic_dust.bucket_domain_name
}
