output "bucket_name" {
  description = "The full name of the created S3 bucket."
  value       = aws_s3_bucket.shelter_bucket.id
}
