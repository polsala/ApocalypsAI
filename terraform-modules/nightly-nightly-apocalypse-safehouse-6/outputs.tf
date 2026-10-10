output "bucket_arn" {
  description = "ARN of the created bucket"
  value       = aws_s3_bucket.safehouse.arn
}

output "read_only_policy_arn" {
  description = "ARN of the read‑only IAM policy"
  value       = aws_iam_policy.read_only.arn
}
