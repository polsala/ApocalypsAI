output "bucket_id" {
  description = "The ID of the S3 bucket."
  value       = aws_s3_bucket.chrono_vault.id
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket."
  value       = aws_s3_bucket.chrono_vault.arn
}

output "bucket_regional_domain_name" {
  description = "The regional domain name of the S3 bucket."
  value       = aws_s3_bucket.chrono_vault.bucket_regional_domain_name
}

output "website_endpoint" {
  description = "The S3 bucket website endpoint (if enabled)."
  value       = var.enable_static_website ? aws_s3_bucket_website_configuration.chrono_vault_website[0].website_endpoint : null
}
