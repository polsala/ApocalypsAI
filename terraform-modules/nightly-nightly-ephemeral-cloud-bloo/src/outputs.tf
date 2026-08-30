output "bucket_id" {
  description = "The ID (name) of the S3 bucket."
  value       = aws_s3_bucket.bloom_bucket.id
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket."
  value       = aws_s3_bucket.bloom_bucket.arn
}

output "bucket_website_endpoint" {
  description = "The S3 bucket website endpoint (if public access is enabled)."
  value       = var.enable_public_access ? aws_s3_bucket_website_configuration.bloom_website_config[0].website_endpoint : null
}

output "lifecycle_rule_id" {
  description = "The ID of the lifecycle rule applied to the bucket."
  value       = aws_s3_bucket_lifecycle_configuration.bloom_lifecycle.rule[0].id
}

output "lifecycle_expiration_days" {
  description = "The number of days after which objects will expire."
  value       = aws_s3_bucket_lifecycle_configuration.bloom_lifecycle.rule[0].expiration[0].days
}
