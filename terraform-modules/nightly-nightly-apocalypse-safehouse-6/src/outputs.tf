output "bucket_id" {
  description = "ID of the created bucket"
  value       = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  description = "ARN of the bucket"
  value       = aws_s3_bucket.safehouse.arn
}

output "policy_arn" {
  description = "ARN of the IAM policy attached to the role"
  value       = aws_iam_policy.safehouse_access.arn
}
