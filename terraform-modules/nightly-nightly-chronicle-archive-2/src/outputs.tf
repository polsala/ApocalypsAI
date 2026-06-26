output "bucket_id" {
  description = "The ID (name) of the S3 bucket."
  value       = aws_s3_bucket.archive.id
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket."
  value       = aws_s3_bucket.archive.arn
}

output "bucket_domain_name" {
  description = "The S3 bucket's regional domain name."
  value       = aws_s3_bucket.archive.bucket_regional_domain_name
}
