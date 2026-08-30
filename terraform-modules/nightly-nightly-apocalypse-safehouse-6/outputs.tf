output "bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.supplies.id
}

output "table_name" {
  description = "Name of the DynamoDB table"
  value       = aws_dynamodb_table.inventory.name
}

output "iam_role_arn" {
  description = "ARN of the IAM role"
  value       = aws_iam_role.safehouse_role.arn
}
