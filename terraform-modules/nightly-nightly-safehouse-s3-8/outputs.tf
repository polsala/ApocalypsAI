output "bucket_id" {
  description = "ID of the bucket"
  value       = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  description = "ARN of the bucket"
  value       = aws_s3_bucket.safehouse.arn
}
