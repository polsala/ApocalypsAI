output "bucket_arn" {
  description = "The ARN of the S3 bucket."
  value       = aws_s3_bucket.reality_anchor_vault.arn
}

output "bucket_id" {
  description = "The ID (name) of the S3 bucket."
  value       = aws_s3_bucket.reality_anchor_vault.id
}

output "bucket_domain_name" {
  description = "The S3 bucket's regional domain name."
  value       = aws_s3_bucket.reality_anchor_vault.bucket_regional_domain_name
}
