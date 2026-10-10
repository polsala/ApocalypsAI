output "bucket_id" {
  description = "The name (ID) of the created S3 bucket."
  value       = aws_s3_bucket.anomaly_beacon.id
}

output "bucket_arn" {
  description = "The ARN of the created S3 bucket."
  value       = aws_s3_bucket.anomaly_beacon.arn
}

output "bucket_domain_name" {
  description = "The S3 bucket's regional domain name."
  value       = aws_s3_bucket.anomaly_beacon.bucket_regional_domain_name
}
