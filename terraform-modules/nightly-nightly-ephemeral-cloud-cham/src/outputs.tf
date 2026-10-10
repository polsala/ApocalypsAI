output "instance_public_ip" {
  description = "The public IP address of the ephemeral EC2 instance."
  value       = aws_instance.ephemeral_server.public_ip
}

output "s3_bucket_name" {
  description = "The name of the ephemeral S3 bucket."
  value       = aws_s3_bucket.ephemeral_storage.bucket
}

output "vpc_id" {
  description = "The ID of the VPC created for the ephemeral environment."
  value       = aws_vpc.main.id
}
