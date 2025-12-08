output "bucket_id" {
  description = "The ID (name) of the S3 bucket."
  value       = aws_s3_bucket.critter_cache.id
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket."
  value       = aws_s3_bucket.critter_cache.arn
}

output "comfort_object_url" {
  description = "The URL to the comfort message object in the bucket."
  value       = "s3://${aws_s3_bucket.critter_cache.id}/${aws_s3_bucket_object.comfort_message_object.key}"
}
