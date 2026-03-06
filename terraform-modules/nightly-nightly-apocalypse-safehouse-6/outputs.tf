output "bucket_id" {
  description = "The bucket name (ID)."
  value       = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  description = "The full ARN of the bucket."
  value       = aws_s3_bucket.safehouse.arn
}
