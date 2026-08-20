output "bucket_id" {\n  description = "The ID of the created S3 bucket."
  value       = aws_s3_bucket.safehouse.id\n}\n\noutput "bucket_arn" {\n  description = "The ARN of the created S3 bucket."
  value       = aws_s3_bucket.safehouse.arn\n}\n\noutput "bucket_name" {\n  description = "The final bucket name (custom or generated)."
  value       = aws_s3_bucket.safehouse.bucket\n}\n
