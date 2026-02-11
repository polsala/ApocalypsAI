output "bucket_id" {
  description = "The ID (name) of the S3 bucket."
  value       = aws_s3_bucket.temporal_beacon.id
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket."
  value       = aws_s3_bucket.temporal_beacon.arn
}

output "bucket_domain_name" {
  description = "The domain name of the S3 bucket."
  value       = aws_s3_bucket.temporal_beacon.bucket_domain_name
}
