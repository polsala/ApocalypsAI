output "website_endpoint" {
  description = "The S3 static website endpoint URL."
  value       = aws_s3_bucket.beacon_bucket.website_endpoint
}

output "bucket_name" {
  description = "The name of the S3 bucket created."
  value       = aws_s3_bucket.beacon_bucket.bucket
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket created."
  value       = aws_s3_bucket.beacon_bucket.arn
}
