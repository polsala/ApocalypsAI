output "bucket_arn" {
  description = "ARN of the created S3 bucket"
  value       = aws_s3_bucket.safehouse.arn
}

output "policy_arn" {
  description = "ARN of the IAM policy granting access"
  value       = aws_iam_policy.safehouse_access.arn
}
