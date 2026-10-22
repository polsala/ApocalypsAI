output "bucket_arn" {
  description = "ARN of the created S3 bucket."
  value       = aws_s3_bucket.safehouse.arn
}

output "supply_cache_key" {
  description = "Key of the placeholder supply cache object."
  value       = aws_s3_bucket_object.supply_cache.key
}
