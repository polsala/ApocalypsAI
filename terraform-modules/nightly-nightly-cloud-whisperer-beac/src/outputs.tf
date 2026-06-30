output "website_endpoint" {
  description = "The URL of the static website endpoint."
  value       = aws_s3_bucket.whisper_beacon.website_endpoint
}

output "bucket_name" {
  description = "The full name of the S3 bucket."
  value       = aws_s3_bucket.whisper_beacon.bucket
}
