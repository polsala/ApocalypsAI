output "bucket_id" {
  description = "The name of the created bucket"
  value       = aws_s3_bucket.safehouse.id
}
