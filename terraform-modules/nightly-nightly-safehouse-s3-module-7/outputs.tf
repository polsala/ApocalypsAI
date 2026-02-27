output "bucket_arn" {
  description = "ARN of the created bucket"
  value       = aws_s3_bucket.safehouse.arn
}
