output "s3_bucket_name" {
  description = "The name of the provisioned S3 bucket."
  value       = aws_s3_bucket.scavenger_bucket.bucket
}

output "ec2_instance_id" {
  description = "The ID of the provisioned EC2 instance."
  value       = aws_instance.scavenger_ec2.id
}

output "lambda_function_name" {
  description = "The name of the provisioned Lambda function."
  value       = aws_lambda_function.scavenger_lambda.function_name
}

output "dynamodb_table_name" {
  description = "The name of the provisioned DynamoDB table."
  value       = aws_dynamodb_table.scavenger_dynamodb.name
}
