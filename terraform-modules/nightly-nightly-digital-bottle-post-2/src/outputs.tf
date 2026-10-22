output "bucket_id" {
  description = "The name (ID) of the S3 bucket."
  value       = aws_s3_bucket.bottle_post_bucket.id
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket."
  value       = aws_s3_bucket.bottle_post_bucket.arn
}

output "bucket_domain_name" {
  description = "The domain name of the S3 bucket."
  value       = aws_s3_bucket.bottle_post_bucket.bucket_domain_name
}
