output "bucket_arn" {\n  description = "ARN of the created S3 bucket"\n  value       = aws_s3_bucket.safehouse.arn\n}
