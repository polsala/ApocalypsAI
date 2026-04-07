output "bucket_id" {
  description = "ID of the created S3 bucket"
  value       = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.safehouse.arn
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  value       = aws_dynamodb_table.supply_cache.name
}
