output "bunker_id" {
  description = "The ID of the S3 bucket (your digital bunker)."
  value       = aws_s3_bucket.data_bunker.id
}

output "bunker_arn" {
  description = "The ARN of the S3 bucket."
  value       = aws_s3_bucket.data_bunker.arn
}

output "kms_key_arn" {
  description = "The ARN of the KMS key used for encryption."
  value       = aws_kms_key.cipher_lock.arn
}
