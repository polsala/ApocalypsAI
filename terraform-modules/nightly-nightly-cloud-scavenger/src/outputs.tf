output "s3_bucket_name" {
  description = "The name of the provisioned S3 data cache bucket."
  value       = var.enable_s3_cache ? aws_s3_bucket.data_cache[0].bucket : "S3 cache not enabled"
}

output "ec2_public_ip" {
  description = "The public IP address of the EC2 communication relay node."
  value       = var.enable_ec2_relay ? aws_instance.relay_node[0].public_ip : "EC2 relay not enabled"
}
