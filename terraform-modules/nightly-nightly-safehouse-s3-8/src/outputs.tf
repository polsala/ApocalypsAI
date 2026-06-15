output "bucket_id" {
  description = "The ID of the created S3 bucket."
  value       = aws_s3_bucket.safehouse.id
}

output "supply_cache_url" {
  description = "URL to the placeholder supply cache object."
  value       = "https://${aws_s3_bucket.safehouse.bucket_regional_domain_name}/supply-cache.txt"
}
