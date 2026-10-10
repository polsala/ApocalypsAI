output "bucket_id" {
  description = "The bucket name."
  value       = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  description = "The bucket ARN."
  value       = aws_s3_bucket.safehouse.arn
}
