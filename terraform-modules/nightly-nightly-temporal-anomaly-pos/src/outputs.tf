output "instance_public_ip" {
  description = "The public IP address of the EC2 instance."
  value       = aws_instance.anomaly_observer.public_ip
}

output "s3_bucket_name" {
  description = "The name of the S3 bucket for anomaly logs."
  value       = aws_s3_bucket.anomaly_log_vault.bucket
}
