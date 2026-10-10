output "bucket_id" {
  description = "The name of the S3 bucket."
  value       = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket."
  value       = aws_s3_bucket.safehouse.arn
}
