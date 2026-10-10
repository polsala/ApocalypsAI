output "bucket_id" {
  description = "The ID of the created bucket"
  value       = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  description = "The ARN of the created bucket"
  value       = aws_s3_bucket.safehouse.arn
}

output "bucket_name" {
  description = "The name of the created bucket"
  value       = aws_s3_bucket.safehouse.bucket
}
