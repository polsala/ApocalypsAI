output "s3_bucket_name" {
  description = "The name of the S3 bucket created for the digital message bottle."
  value       = aws_s3_bucket.message_bottle.id
}

output "dynamodb_table_name" {
  description = "The name of the DynamoDB table created for message metadata.""
  value       = aws_dynamodb_table.message_metadata.name
}
