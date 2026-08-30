output "bucket_id" {
  description = "The ID of the bucket"
  value       = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  description = "The ARN of the bucket"
  value       = aws_s3_bucket.safehouse.arn
}
