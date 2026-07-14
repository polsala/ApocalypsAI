output "bucket_id" {
  description = "The ID of the created S3 bucket."
  value       = aws_s3_bucket.supply_cache.id
}

output "bucket_arn" {
  description = "The ARN of the created S3 bucket."
  value       = aws_s3_bucket.supply_cache.arn
}
