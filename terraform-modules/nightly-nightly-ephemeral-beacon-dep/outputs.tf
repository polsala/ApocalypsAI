output "beacon_bucket_name" {
  description = "The name of the S3 bucket beacon."
  value       = aws_s3_bucket.beacon_bucket.id
}

output "beacon_whisper_url" {
  description = "The public URL of the 'whisper' content (whisper.txt) in the S3 bucket."
  value       = "https://${aws_s3_bucket.beacon_bucket.id}.s3.${var.aws_region}.amazonaws.com/${aws_s3_bucket_object.beacon_whisper.key}"
}
