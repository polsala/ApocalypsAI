output "bucket_name" {
  description = "The name of the created bucket."
  value       = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  description = "ARN of the bucket."
  value       = aws_s3_bucket.safehouse.arn
}
