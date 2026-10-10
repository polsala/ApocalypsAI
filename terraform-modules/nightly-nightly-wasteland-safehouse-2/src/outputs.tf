output "bucket_id" {
  description = "The ID of the created S3 bucket."
  value       = aws_s3_bucket.safehouse.id
}

output "supply_object_key" {
  description = "Key of the initial supply cache object."
  value       = aws_s3_bucket_object.supply_cache.key
}
