output "public_ip" {
  description = "The public IP address of the EC2 beacon instance."
  value       = aws_instance.beacon.public_ip
}

output "s3_bucket_name" {
  description = "The name of the S3 bucket created for beacon logs/messages."
  value       = aws_s3_bucket.beacon_logs.bucket
}

output "security_group_id" {
  description = "The ID of the security group created for the beacon."
  value       = aws_security_group.beacon_sg.id
}
