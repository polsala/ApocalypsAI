output "bucket_id" {
  description = "The ID (name) of the S3 bucket."
  value       = aws_s3_bucket.echo_chamber.id
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket."
  value       = aws_s3_bucket.echo_chamber.arn
}
