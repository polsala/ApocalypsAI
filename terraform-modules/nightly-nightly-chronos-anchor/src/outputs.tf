output "bucket_arn" {
  description = "The ARN of the created S3 bucket."
  value       = aws_s3_bucket.chronos_anchor_bucket.arn
}

output "bucket_id" {
  description = "The ID (name) of the created S3 bucket."
  value       = aws_s3_bucket.chronos_anchor_bucket.id
}

output "chronos_epoch" {
  description = "The Unix timestamp (epoch) when the resource was provisioned."
  value       = floor(timestamp())
}
