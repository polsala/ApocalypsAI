output "bucket_id" {
  description = "The ID of the created bucket"
  value       = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  description = "The ARN of the created bucket"
  value       = aws_s3_bucket.safehouse.arn
}

output "access_key_id" {
  description = "IAM access key ID for the generated user"
  value       = aws_iam_access_key.safehouse_key.id
}

output "secret_access_key" {
  description = "IAM secret access key (sensitive)"
  value       = aws_iam_access_key.safehouse_key.secret
  sensitive   = true
}
