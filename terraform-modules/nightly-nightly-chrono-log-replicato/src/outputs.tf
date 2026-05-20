output "bucket_id" {
  description = "The ID of the created S3 bucket."
  value       = aws_s3_bucket.chrono_log_bucket.id
}

output "bucket_arn" {
  description = "The ARN of the created S3 bucket."
  value       = aws_s3_bucket.chrono_log_bucket.arn
}

output "iam_policy_arn" {
  description = "The ARN of the IAM policy created for chrono-log write access."
  value       = aws_iam_policy.chrono_log_write_policy.arn
}
