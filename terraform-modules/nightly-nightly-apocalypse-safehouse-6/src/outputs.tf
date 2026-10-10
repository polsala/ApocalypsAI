output "bucket_arn" {
  description = "ARN of the created S3 bucket."
  value       = aws_s3_bucket.safehouse.arn
}

output "read_only_policy_arn" {
  description = "ARN of the IAM policy granting read‑only access to the bucket."
  value       = aws_iam_policy.read_only_policy.arn
}
