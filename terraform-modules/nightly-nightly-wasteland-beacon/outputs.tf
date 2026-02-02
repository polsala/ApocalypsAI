output "beacon_public_ip" {
  description = "The public IP address of the Wasteland Beacon EC2 instance."
  value       = aws_instance.beacon_ec2.public_ip
}

output "beacon_s3_bucket_name" {
  description = "The name of the S3 bucket for beacon messages."
  value       = aws_s3_bucket.beacon_storage.bucket
}

output "beacon_s3_bucket_endpoint" {
  description = "The endpoint URL for the S3 bucket."
  value       = aws_s3_bucket.beacon_storage.bucket_regional_domain_name
}
