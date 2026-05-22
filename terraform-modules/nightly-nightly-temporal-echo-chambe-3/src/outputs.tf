output "bucket_id" {
  description = "The ID (name) of the Temporal Echo Chamber S3 bucket."
  value       = aws_s3_bucket.echo_chamber.id
}

output "bucket_arn" {
  description = "The ARN of the Temporal Echo Chamber S3 bucket."
  value       = aws_s3_bucket.echo_chamber.arn
}

output "bucket_domain_name" {
  description = "The S3 bucket domain name, useful for direct access."
  value       = aws_s3_bucket.echo_chamber.bucket_domain_name
}
