output "bucket_endpoint" {
  description = "The HTTP endpoint for the S3 bucket."
  value       = "http://${aws_s3_bucket.message_bottle.bucket}.s3.amazonaws.com"
}

output "initial_message_url" {
  description = "The URL to the initial message object."
  value       = "http://${aws_s3_bucket.message_bottle.bucket}.s3.amazonaws.com/${aws_s3_bucket_object.initial_message.key}"
}
