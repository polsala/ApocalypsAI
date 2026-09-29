output "beacon_public_ip" {
  description = "The public IP address of the Cloud Beacon."
  value       = aws_eip.beacon_eip.public_ip
}

output "beacon_url" {
  description = "The URL to access the Cloud Beacon."
  value       = "http://${aws_eip.beacon_eip.public_ip}"
}

output "s3_bucket_name" {
  description = "The name of the S3 bucket for beacon message archives."
  value       = aws_s3_bucket.beacon_message_archive.bucket
}
